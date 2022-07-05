import configparser
from datetime import datetime, timedelta
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.types import DateType, IntegerType



config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['DEFAULT']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['DEFAULT']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """ Create spark session """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages","org.apache.hadoop:hadoop-aws:2.7.0")\
        .getOrCreate()
    return spark


def process_immigration_data(spark, input_data, output_data):
    """
    Loads I94 Immigration data from S3,
    extracts columns to create the I94 table, and 
    writes data back to S3.
    """

    # get filepath to I94 immigration data
    immigration_data = input_data + "sas_data/*.parquet"

    # read I94 data 
    df_immigration = spark.read.parquet(immigration_data)

    # extract columns to create I94 table
    immigration_table = df_immigration.select('cicid', 'i94yr', 'i94mon', 'i94cit', 'i94res', 'i94port', 'arrdate',
       'i94mode', 'i94addr', 'depdate', 'i94bir', 'i94visa', 'count',
       'dtadfile', 'entdepa', 'entdepd', 'matflag', 'biryear', 'dtaddto',
       'gender', 'airline', 'admnum', 'fltno', 'visatype').distinct()

    # create a udf to convert arrival & departure date in SAS format to datetime object
    get_datetime = udf(lambda x: (datetime(1960, 1, 1).date() + timedelta(x)).isoformat() if x else None)
    immigration_table = immigration_table.withColumn("arrdate", get_datetime('arrdate').cast(DateType())) \
        .withColumn("depdate", get_datetime('depdate').cast(DateType()))
    
    # print statements for debugging
    immigration_table.show() 
    immigration_table.printSchema()

    # write immigration data to parquet files 
    immigration_table.write.mode("overwrite").parquet(os.path.join(output_data, 'immigration'))


def process_port_locations(spark, input_data, output_data):
    """
    Loads I94_SAS_Labels_Description from S3,
    extracts columns to create the port_location table, and 
    writes data back to S3.
    """
    port_locations = input_data + "I94_SAS_Labels_Descriptions.csv"

    # read port locations file
    df_port_location = spark.read.format("csv").option("header","true").load(port_locations)
    df_port_location = df_port_location.select('port_code','port_city', 'port_state')

    df_port_location.show() # print statement for debugging

    df_port_location.write.mode("overwrite").parquet(os.path.join(output_data, 'port_locations'))


def process_airport_codes(spark, input_data, output_data):
    """
    Loads airport_code data from S3,
    extracts columns to create the airport_code table, and 
    writes data back to S3.
    """

    # get filepath to airport codes data
    airport_codes = input_data + "airport-codes_csv.csv"

    # read airport code data
    df_airport_code = spark.read.format("csv").option("header","true").load(airport_codes)
    airport_code_table = df_airport_code.na.drop(subset=["iata_code"])
    airport_code_table = airport_code_table.withColumn("elevation_ft", airport_code_table['elevation_ft'].cast('float'))

    # print statements for debugging
    airport_code_table.show()
    airport_code_table.printSchema()

    # write clean airport_code_table to parquet files
    airport_code_table.write.mode("overwrite").parquet(os.path.join(output_data, 'airport_code'))


def process_temp(spark, input_data, output_data):
    """
    Loads temperature data from S3,
    extracts columns to create the temperature table, and 
    writes data back to S3.
    """
    # get filepath to temp data 
    temp_data = input_data + "GlobalLandTemperaturesByCity.csv"

    # read temp data using spark
    df_temp_data = spark.read.format("csv").option("header","true").load(temp_data)
    df_temp_data = df_temp_data.where(df_temp_data['Country'] == 'United States')
    
    # rename columns
    df_temp_data = df_temp_data.withColumnRenamed("AverageTemperature", "average_temperature") \
        .withColumnRenamed("AverageTemperatureUncertainty", "average_temperature_uncertainty")

    # change column datatypes
    df_temp_data = df_temp_data.withColumn("average_temperature", df_temp_data['average_temperature'].cast('float')) \
        .withColumn("average_temperature_uncertainty", df_temp_data['average_temperature_uncertainty'].cast('float')) \
            .withColumn("dt", df_temp_data["dt"].cast(DateType()))

    df_temp_data.show() # print statement for debugging
    df_temp_data.printSchema()

    df_temp_data.write.mode("overwrite").parquet(os.path.join(output_data, 'temperature'))


def process_demographics(spark, input_data, output_data):
    """
    Loads demographics data from S3,
    extracts columns to create the demographics table, and 
    writes data back to S3.
    """
    # get filepath to demographics data 
    demographics_data = input_data + "us-cities-demographics.csv"

    # read temp data using spark
    df_demographics = spark.read.format("csv").options(header=True, delimiter=";").load(demographics_data)

    df_demographics_data = df_demographics.withColumn("id", monotonically_increasing_id())\
        .select(['id', 'City', 'State', 'Male Population', 'Female Population', 'Total Population', 'Average Household Size', \
            'Number of Veterans', 'Foreign-born', 'State Code', 'Race', 'Count']).distinct() 

    new_columns = ['id', 'city', 'state', 'male_population', 'female_population', 'total_population', 'average_household_size',\
                   'num_veterans', 'foreign_born', 'state_code', 'race', 'count']

    df_demographics_data = df_demographics_data.toDF(*new_columns)

    df_demographics_data = df_demographics_data.withColumn("male_population", df_demographics_data['male_population'].cast(IntegerType())) \
        .withColumn("female_population", df_demographics_data['female_population'].cast(IntegerType())) \
        .withColumn("total_population", df_demographics_data['total_population'].cast(IntegerType())) \
        .withColumn("average_household_size", df_demographics_data['average_household_size'].cast('float')) \
        .withColumn("num_veterans", df_demographics_data['num_veterans'].cast(IntegerType())) \
        .withColumn("foreign_born", df_demographics_data['foreign_born'].cast(IntegerType())) \
        .withColumn("count", df_demographics_data['count'].cast(IntegerType()))

    
    df_demographics_data.show() # print statement for debugging
    df_demographics_data.printSchema()

    df_demographics_data.write.mode("overwrite").parquet(os.path.join(output_data, 'demographics'))


def main():
    print("Creating spark session..")
    spark = create_spark_session()
    input_data = "s3a://data-eng-capstone-project/"
    output_data = "s3a://data-eng-capstone-project/staging_area/"
    print("spark session created")
    process_immigration_data(spark, input_data, output_data)   
    process_port_locations(spark, input_data, output_data) 
    process_airport_codes(spark, input_data, output_data)
    process_temp(spark, input_data, output_data)
    process_demographics(spark, input_data, output_data)
    



if __name__ == "__main__":
    main()