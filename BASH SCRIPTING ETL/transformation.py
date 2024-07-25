# Importing libraries
import pandas as pd
from snowflake.connector import connect

# Snowflake connection details 
SNOWFLAKE_ACCOUNT = "SNOWFLAKE_ACCOUNT"
SNOWFLAKE_USER = "SNOWFLAKE_USER"
SNOWFLAKE_PASSWORD = "SNOWFLAKE_PASSWORD"
SNOWFLAKE_DATABASE = "SNOWFLAKE_DB"
SNOWFLAKE_SCHEMA = "SNOWFLAKE_SCHEMA_NAME"
SNOWFLAKE_ROLE = "SNOWFLAKE_ACCOUNT_ROLE"

def transform_and_load(data_file):
    try:

        airport_data = pd.read_csv(data_file, delimiter=",", header=None)
        final_data = airport_data.iloc[:, :3]

        final_data.to_csv("airport_data_processed.csv", index=False)

        print('Final Airport data :', final_data)
        # Connect to Snowflake
        ctx = connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE
        )

        # Create a cursor object
        cur = ctx.cursor()

        # Creating stage
        sql_stmt_create_stage = """
        CREATE OR REPLACE STAGE airport_data_stage;
        """
        cur.execute(sql_stmt_create_stage)

        # Loading data to stage
        stage_file_data = """
        PUT 'file:////Users/valhalla/Documents/UW,\ Pace/Data Acquisition and Management AI/Assignment3/airport_data_processed.csv' @airport_data_stage AUTO_COMPRESS = TRUE;
        """
        cur.execute(stage_file_data)

        # Create SQL statement
        create_sql_stmt = """
        CREATE OR REPLACE TABLE MOHAN_AI2024.ASSIGNMENT3.AIRPORT_TBL(
        ID TEXT,
        NAME TEXT,
        LOCATION TEXT
        );
        """
        cur.execute(create_sql_stmt)
        
        # Creating file format
        create_file_format ="""
        create or replace file format MOHAN_AI2024.ASSIGNMENT3.AIRPORT_CSV_COMMA_FILE
            type = 'CSV' 
            field_delimiter = ','
            skip_header = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"';
        """
        cur.execute(create_file_format)

        # Upload data to stage
        sql_stmt_copy_data = """
        COPY INTO MOHAN_AI2024.ASSIGNMENT3.AIRPORT_TBL
        FROM @airport_data_stage
        FILES = ('airport_data_processed.csv.gz')
        FILE_FORMAT = (FORMAT_NAME = MOHAN_AI2024.ASSIGNMENT3.AIRPORT_CSV_COMMA_FILE);
        """
        cur.execute(sql_stmt_copy_data)

        # Removing stage file
        sql_remove_stage = """REMOVE @airport_data_stage"""
        cur.execute(sql_remove_stage)
        
        # Commit the changes
        ctx.commit()
        
        if cur:
            cur.close()
        if ctx:
            ctx.close()
        
        print("ETL SUCCESSFULLY DONE!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Main function
if __name__ == "__main__":
    transform_and_load("airports.dat")


