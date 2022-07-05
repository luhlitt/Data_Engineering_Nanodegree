**Enabling US Immigration Analytics with Apache Spark and Amazon
Redshift**

**Overview**

This project is part of the Udacity Data Engineering Nanodegree program.
The objective is to build an ETL pipeline that combines disparate
sources of data, transforms them, and loads them into a data warehouse
to be used for analytics.

In this project, US Immigration data is combined with other data sources
to create data models that can be analysed. To accomplish this, Apache
Spark running on Amazon EMR is used to extract and process the data into
analytics tables, before loading it back into Amazon S3, and Amazon
Redshift is used for analysis.

Some of the questions aimed to be answered by the final model are:

1.  How does seasonality affect visitor arrivals?

2.  Which cities receives the most tourists?

3.  Do immigrants tend to flock to cities with a higher immigrant
    population?

**Architecture**

At a high level, the solution includes the following steps:

Step 1 is to ingest datasets:

-   Download publicly available US Immigration [I94 Immigration
    Data](https://www.trade.gov/national-travel-and-tourism-office),
    [WorldTemperature
    Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data),
    [U.S City Demographic
    Data](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/) 
    and [Airport Code
    Table](https://datahub.io/core/airport-codes#data) datasets and
    stage them in Amazon S3.

Step 2 is to enrich data by using ETL:

1.  Transform both the arrival date and departure columns in the
    immigration table from SAS date format to datetime by using a
    user-defined function in Spark.

2.  Parse the I94_SAS_Labels_descriptions file to derive additional
    table port_locations. This derived table will allow for the I94
    immigration table to be joined with other datasets through the port
    code and city columns.

3.  For the other datasets, rename columns and change data types to
    match preferred format.

4.  After the transformation process, the data is loaded back into S3 as
    Parquet files.

Step 3 is to load the data to Amazon Redshift:

-   In this last step, the enriched data is loaded from S3 to Redshift
    using the COPY command.

**Diagram of the architecture.**

![Diagram Description automatically
generated](./media/image1.jpg)

1 Solution Architecture

**Data Sources**

**I94 Immgiration Data**

From the [US National Tourism and Trade
Office](https://www.trade.gov/national-travel-and-tourism-office) page.
The data contains non-immigrant arrival statistics such as the visa
type, port of entry, demographics, mode of transportation, etc. The
format is in SAS. In addition, a data dictionary
I94_SAS_Labels_Description was provided in Udacity workspace for the
immigration data.

To combine the immigration dataset with other datasets used, the port
code, city and state field were extracted from the
I94_SAS_Labels_Description file.

**World Temperature Data**

From
[Kaggle](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
website. The data downloaded is the GloablLandTemperaturesByCity csv. It
contains land temperatures by city. Data format is CSV

**Airport Code Data**

From [here](https://datahub.io/core/airport-codes#data). It is a simple
table of airport codes and corresponding cities. Data format is CSV

**U.S City Demographics Data**

From
[OpenSoft](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).
It contains information about demographics of all US cities and
census0designated places with a population greater or equal to 65,000.
Data format is CSV

**Data Model**

Since the overall objective of this project is for powering analytics, a
star schema is used to structure the database. The database has 5
tables, the immigration, temperature, airport_code, demographics, and
port_location. The tables can be joined to each other using the
port_code (also named as iata_code in some tables), and city columns.

![Diagram Description automatically
generated](./media/image2.png)

Refer to `data_dictionary.md` for data_dictionary.
**2** ERD

**Data Pipeline Build Up Steps**

1.  Use Pandas to explore datasets and perform pre-processing steps. An
    additional table was derived from the I94_SAS_Labels_Description
    file and converted to a csv file, refer to `Capstone Project
    Template.ipynb`.

2.  Conceptually map out the data model.

3.  Manually upload all datasets to an S3 bucket.

4.  Extract, clean and process datasets to create analytics table with
    Spark, `etl.py`

    a.  Processing steps such as renaming and converting column types to
        date and integer formats were carried out.

5.  After processing, load enriched data back to S3 as parquet files,
    `etl.py`

6.  Create tables in Redshift, `create_tables.py`

7.  Load data from S3 to Redshift, `load_to_redshift.py`

8.  Perform data quality checks to ensure the pipeline ran as expected,
    `data_check.py`

    a.  Check there are no empty tables after running ETL pipeline

**Tools and Technologies**

The main technologies used are:

-   **Python Pandas** - is used for data exploration and pre-processing

-   **Apache Spark -** is used to extract, clean, and transform the
    datasets. Although it is primarily used for big data sets. I chose
    to use this tool to learn how to manipulate datasets using Spark.

-   **AWS S3 -** for data storage

-   **Amazon EMR** - to run Spark clusters.

-   **Amazon Redshift** - as the database for analysis.

**Data Update Frequency**

The I94 data describes US non-immigration arrival events aggregated
monthly. As a result, it is recommended the data is updated monthly.

**Future Design Considerations**

1.  If the data was increased by 100x.

    AWS EMR is a distributed data cluster for processing big data and can be scaled as needed.

2.  If the pipelines were run daily by 7am.

    If the pipeline were run daily, a production data pipeline will be used using Apache Airflow to write DAGs that will run on a schedule.

3.  If the database needed to be accessed by 100+ people.

    Amazon Redshift can handle up to 500 concurrent connections per cluster and can be scaled as needed.

**Analysis**

1.  Is there a relationship between the number of immigrant visits to
    states with a higher immigrant population?

    From the chart below, we can see that states with high immigrant
    population also tend to have high number of tourists.

    ![Chart, line chart, histogram Description automatically
    generated](./media/image3.png)

    ```
    with demo as (
    select 
        distinct
        d.state_code,
        avg(d.foreign_born) as avg_foreign_born,
            sum(d.foreign_born) as sum_foreign_born
    from demographics d
    group by 1
    order by 2 desc
        ),
    top_state as (   
    select 
        distinct addr,
        count(*) as num_tourists
    from immigration 
    group by 1 
    order by 2 desc
        )
        
    select 
        distinct ts.addr,
        ts.num_tourists,
        de.avg_foreign_born
    from top_state ts 
    left join demo de on de.state_code = ts.addr
    where de.sum_foreign_born > avg_foreign_born
    order by 2 desc
    ```

2.  Which cities are the most visited by tourists?

    Topmost visited cities in 2016.

    ![Chart, bar chart Description automatically
    generated](./media/image4.png)

    ```
    select 
        distinct port as port_of_entry,
        port_city as city,
        count(*) as number_of_tourists
    from immigration i
    left join port_locations pl 
        on pl.port_code = i.port
    group by 1,2
    order by 3 desc
    limit 5
    ```

    Top 5 business travel destinations in the U.S in 2016

    ![Chart, bar chart Description automatically
    generated](./media/image5.png)

    ```
    select 
        distinct port as port_of_entry,
        port_city as city,
        count(*) as number_of_tourists
    from immigration i
    left join port_locations pl 
        on pl.port_code = i.port
    where visatype = 'F1'
    group by 1,2
    order by 3 desc
    limit 5
    ```