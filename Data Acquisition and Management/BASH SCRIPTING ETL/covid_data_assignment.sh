echo "Loading the Data into a CSV file"

curl -o owid-covid-data.csv https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv

echo "Extracting 1,2,4, and 5 columns into a new file to perform the operations."

cut -d ',' -f 1,2,4,5 owid-covid-data.csv >  covid_data.csv

echo  "Printing the last 5 Data from the selected columns from the CSV file"

tail -n 5 covid_data.csv

snowsql -c mohan_bash_assignment<< EOF  

-- 1. Updating role, 
use role ACCOUNTADMIN;

-- 2. Creating COVID_RECORD table
CREATE OR REPLACE TABLE MOHAN_AI2024.ASSIGNMENT3.COVID_RECORD (
    isocode VARCHAR(100),
    continent VARCHAR(100),
    case_date VARCHAR(100),
    total_cases DECIMAL
); 

-- 3. Creating stage file
CREATE OR REPLACE STAGE MOHAN_CSV_STAGE;

-- 4. Loading local file to stage
PUT 'file:////Users/valhalla/Documents/UW,\ Pace/Data Acquisition and Management AI/Assignment3/covid_data.csv' @MOHAN_CSV_STAGE AUTO_COMPRESS = TRUE;

-- 5. Creating file format for CSV file
create or replace file format MOHAN_AI2024.ASSIGNMENT3.CSV_COMMA_FILE
    type = 'CSV' 
    field_delimiter = ',' 
    skip_header = 1;

-- 6. Loading stage file data to COVID_RECORD table 
COPY INTO MOHAN_AI2024.ASSIGNMENT3.COVID_RECORD
        FROM @MOHAN_CSV_STAGE
        FILES = ('covid_data.csv.gz')
        FILE_FORMAT = (FORMAT_NAME = MOHAN_AI2024.ASSIGNMENT3.CSV_COMMA_FILE);

-- 7. Checking COVID_RECORD table record
SELECT * 
FROM MOHAN_AI2024.ASSIGNMENT3.COVID_RECORD 
LIMIT 10;

--8. Removing stage file
REMOVE @MOHAN_CSV_STAGE
EOF

if [ $? -ne 0 ]; then
  echo "Failed to perform data ETL in Snowflake."
  exit 1
fi

echo "SNOWFLAKE ETL successful!"

rm -f owid-covid-data.csv covid_data.csv
