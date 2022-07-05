import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dl.cfg')

ROLE_ARN = config.get("IAM_ROLE", "ARN")
IMMIGRATION_STAGING = config.get("S3", "IMMIGRATION_STAGING")
PORT_LOCATIONS = config.get("S3", "PORT_LOCATIONS")
AIRPORT_CODE = config.get("S3", "AIRPORT_CODE")
TEMPERATURE = config.get("S3", "TEMPERATURE")
DEMOGRAPHICS = config.get("S3", "DEMOGRAPHICS")


# DROP TABLES

immigration_table_drop = "DROP TABLE IF EXISTS immigration"
port_locations_table_drop = "DROP TABLE IF EXISTS port_locations"
airprot_code_table_drop = "DROP TABLE IF EXISTS airport_code"
temperature_table_drop = "DROP TABLE IF EXISTS temperature"
demographics_table_drop = "DROP TABLE IF EXISTS demographics"


# CREATE TABLES

immigration_table_create = (""" 
    CREATE TABLE IF NOT EXISTS immigration(
    cicid       FLOAT PRIMARY KEY,
    year        FLOAT,
    month       FLOAT,
    cit         FLOAT,
    res         FLOAT,
    port        VARCHAR(3),
    arrdate     DATE,
    mode        FLOAT,
    addr        VARCHAR,
    depdate     DATE,
    bir         FLOAT,      
    visa        FLOAT,
    count       FLOAT,
    dtadfile    VARCHAR,
    entdepa     VARCHAR(1),
    entdepd     VARCHAR(1),
    matflag     VARCHAR(1),
    biryear     FLOAT,
    dtaddto     VARCHAR,
    gender      VARCHAR(1),
    airline     VARCHAR,
    admnum      FLOAT,
    fltno       VARCHAR,
    visatype    VARCHAR
);
""")

port_locations_table_create = (""" 
    CREATE TABLE IF NOT EXISTS port_locations (
    id          bigint identity(0, 1), 
    port_code   VARCHAR(3),
    port_city   VARCHAR,
    port_state  VARCHAR         
);
""")

airport_code_table_create = (""" 
    CREATE TABLE IF NOT EXISTS airport_code ( 
    ident        VARCHAR,
    type         VARCHAR,
    name         VARCHAR,
    elevation_ft FLOAT,
    continent    VARCHAR,
    iso_country  VARCHAR,
    iso_region   VARCHAR,
    municipality VARCHAR,
    gps_code     VARCHAR, 
    iata_code    VARCHAR PRIMARY KEY,
    local_code   VARCHAR,
    coordinates  VARCHAR
               
);
""")

temperature_table_create = (""" 
    CREATE TABLE IF NOT EXISTS temperature (
    timestamp                      DATE,
    average_temperature            FLOAT,
    average_temperature_uncertainty FLOAT,
    city                           VARCHAR,
    country                        VARCHAR,
    latitude                       VARCHAR,
    longitude                      VARCHAR           
);
""")

demographics_table_create = (""" 
    CREATE TABLE IF NOT EXISTS demographics (
    id                     BIGINT PRIMARY KEY,
    city                   VARCHAR,
    state                  VARCHAR,
    male_population        INT,
    female_population      INT,
    total_population       INT,
    average_household_size FLOAT,
    num_veterans           INT,
    foreign_born           INT,
    state_code             VARCHAR(2),
    race                   VARCHAR,
    count                  INT
);
""")


# STAGING TABLES

immigration_copy = (""" 
    copy immigration 
    from {}
    credentials 'aws_iam_role={}'
    format as parquet 
    compupdate off 
""").format(IMMIGRATION_STAGING, ROLE_ARN)

port_locations_copy = (""" copy port_locations 
    from {}
    credentials 'aws_iam_role={}'
    format as parquet 
    compupdate off 
""").format(PORT_LOCATIONS, ROLE_ARN)

airport_code_copy = (""" copy airport_code 
    from {}
    credentials 'aws_iam_role={}'
    format as parquet 
    compupdate off 
""").format(AIRPORT_CODE, ROLE_ARN)

temperature_copy = (""" copy temperature 
    from {}
    credentials 'aws_iam_role={}'
    format as parquet 
    compupdate off 
""").format(TEMPERATURE, ROLE_ARN)

demographics_copy = (""" copy demographics 
    from {}
    credentials 'aws_iam_role={}'
    format as parquet 
    compupdate off 
""").format(DEMOGRAPHICS, ROLE_ARN)


# QUERY LISTS

create_table_queries = [immigration_table_create, port_locations_table_create, airport_code_table_create, temperature_table_create, demographics_table_create]
drop_table_queries = [immigration_table_drop, port_locations_table_drop, airprot_code_table_drop, temperature_table_drop, demographics_table_drop]
copy_table_queries = [immigration_copy, port_locations_copy, airport_code_copy, temperature_copy, demographics_copy]

