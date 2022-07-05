**Immigration table**

| **column name** | **type**   | **description**                                                                                |
|-----------------|------------|------------------------------------------------------------------------------------------------|
| cicid           | FLOAT      | PRIMARY KEY                                                                                    |
| year            | FLOAT      | Visitor year of arrival                                                                        |
| month           | FLOAT      | Visitor month of arrival                                                                       |
| cit             | FLOAT      | Visitor country of citizenship (3 digit code of origin city)                                   |
| res             | FLOAT      | Visitor country of citizenship (3 digit code of origin city)                                   |
| port            | VARCHAR(3) | Port of entry (3 digit code). Foreign key --\> port_location.port_code, airport_code.iata_code |
| arrdate         | DATE       | Visitor arrival date in the US                                                                 |
| mode            | FLOAT      | Mode of transportation (1=Air, 2=Sea, 3=Land, 9=Not Supported                                  |
| addr            | VARCHAR    | Arrival state. Foreign key --\> demographics.state_code                                        |
| depdate         | DATE       | Visitor departure date from the U.S.                                                           |
| bir             | FLOAT      | Age of Respondent in Years                                                                     |
| visa            | FLOAT      | Visa codes collapsed into three categories: 1 = Business, 2 = Pleasure, 3 = Student            |
| count           | FLOAT      | Used for summary statistics                                                                    |
| dtadfile        | VARCHAR    | Character Date Field - Date added to I-94 Files                                                |
| entdepa         | VARCHAR(1) | Arrival Flag - admitted or paroled into the U.S.                                               |
| entdepd         | VARCHAR(1) | Departure Flag - Departed, lost I-94 or is deceased                                            |
| matflag         | VARCHAR(1) | Match flag - Match of arrival and departure records                                            |
| biryear         | FLOAT      | 4 digit year of birt                                                                           |
| dtaddto         | VARCHAR    | Character Date Field - Date to which admitted to U.S. (allowed to stay until)                  |
| gender          | VARCHAR(1) | Visitor sex                                                                                    |
| airline         | VARCHAR    | Airline used to arrive in U.S.                                                                 |
| admnum          | FLOAT      | Admission Number                                                                               |
| fltno           | VARCHAR    | Flight number of Airline used to arrive in U.S.                                                |
| visatype        | VARCHAR    | Class of admission legally admitting the non-immigrant to temporarily stay in U.S.             |

**Port_location table**

| **column name** | **type**             | **description**                                                                   |
|-----------------|----------------------|-----------------------------------------------------------------------------------|
| id              | bigint identity(0,1) | Primary Key                                                                       |
| port_code       | VARCHAR(3)           | 3 digit port code. Foreign key --\> immigration.port_code, airport_code.iata_code |
| port_city       | VARCHAR              | Port city                                                                         |
| port_state      | VARCHAR              | Port state (2 digit code) Foreign key --\> temperature.city                       |

**Airport_code table**

| **column name** | **type** | **description**                                                                                    |
|-----------------|----------|----------------------------------------------------------------------------------------------------|
| ident           | VARCHAR  | 4 letter code used for airports that do not have an IATA airport code                              |
| type            | VARCHAR  | Airport type: heliport,small_airport,closed,seaplane_base,balloonport,medium_airport,large_airport |
| name            | VARCHAR  | Airport name                                                                                       |
| elevation_ft    | FLOAT    | Elevation of the airport from sea level                                                            |
| continent       | VARCHAR  | Code for continent of the Airport: NaN, OC, AF, AN, EU, AS, SA                                     |
| iso_country     | VARCHAR  | Airport country code                                                                               |
| iso_region      | VARCHAR  | Airport region code                                                                                |
| municipality    | VARCHAR  | Airport city Foreign key --\> temperature.city                                                     |
| gps_code        | VARCHAR  | Airport GPS code                                                                                   |
| iata_code       | VARCHAR  | Airport code (3 digit code) Primary key and Foreign key --\> immigration.port                      |
| local_code      | VARCHAR, |                                                                                                    |
| coordinates     | VARCHAR  | Airport coordinates lat., long.                                                                    |

**Temperature table**

| **Column**                      | **type** | **description**                                |
|---------------------------------|----------|------------------------------------------------|
| timestamp                       | DATE     | starts in 1750 for average land temperature    |
| average_temperature             | FLOAT    | global average land temperature in celsius     |
| average_temperature_uncertainty | FLOAT    | the 95% confidence interval around the average |
| city                            | VARCHAR  | city. Foreign Key --\> port_location.city      |
| country                         | VARCHAR  | country                                        |
| latitude                        | VARCHAR  | lat                                            |
| longitude                       | VARCHAR  | long                                           |

**Demographics table**

| **column name**        | **type**    | **description**                                               |
|------------------------|-------------|---------------------------------------------------------------|
| Id                     | BIGINT      | Primary Key                                                   |
| city                   | VARCHAR     | city. Foreign Key --\> temperature.city, aiport.municipality. |
| state                  | VARCHAR     | state                                                         |
| male_population        | INT         | male population in the city                                   |
| female_population      | INT         | female population in the city                                 |
| total_population       | INT         | total population                                              |
| average_household_size | FLOAT       | average household size                                        |
| num_veterans           | INT         | number of veterans                                            |
| foreign_born           | INT         | number of foreign born residents                              |
| state_code             | VARCHAR(2)  | state code. Foreign Key --\> Immigration.addr.                |
| race                   | VARCHAR     | race                                                          |
| count                  | INT         | used for summary statistics.                                  |
