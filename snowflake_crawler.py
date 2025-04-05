import snowflake.connector

# Snowflake Connection Details
SNOWFLAKE_CONFIG = {
    "user": "IGBOWEEFE",
    "password": "Arsenals123@SArsenals123@S",  # Consider using environment variables
    "account": "mgwuigb-ee57826",  
    "warehouse": "COMPUTE_WH",
    "database": "HOSPITAL_RAW",
    "schema": "RAW_DATA"
}

# Define stage name and file format
STAGE_NAME = "RAW_HOSPITAL_STAGE"
FILE_FORMAT = "csv_format"  # Ensure this file format is defined in Snowflake

# Connect to Snowflake
conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
cur = conn.cursor()

# Step 1: Get List of CSV Files in the Stage
list_files_query = f"LIST @{STAGE_NAME};"
cur.execute(list_files_query)
raw_files = cur.fetchall()  # Store the result
print(f"Full raw output: {raw_files}")

# Extract filenames from the stored result
files = [row[0].split("/")[-1] for row in raw_files 
         if row[0].endswith(".csv") or row[0].endswith(".csv.gz")]
print(f"Found {len(files)} CSV files in stage: {files}")

# Step 2: Loop Through Files and Infer Schema
for file in files:
    print(f"Processing file: {file}")

    infer_schema_query = f"""
        SELECT * FROM TABLE(
            INFER_SCHEMA(
                LOCATION => '@{STAGE_NAME}/{file}',
                FILE_FORMAT => '{FILE_FORMAT}'
            )
        );
    """
    cur.execute(infer_schema_query)
    schema_info = cur.fetchall()
    print(f"Schema for {file}: {schema_info}")

    if not schema_info:
        print(f"⚠️ No schema detected for {file}. Skipping table creation.")
        continue

    # Generate table name by stripping file extension
    if file.endswith(".csv.gz"):
        table_name = file[:-7]
    elif file.endswith(".csv"):
        table_name = file[:-4]
    table_name = table_name.replace("-", "_").lower()
    columns = ", ".join([f'"{col[0]}" {col[1]}' for col in schema_info])
    
    create_table_query = f"""
        CREATE OR REPLACE TABLE {table_name} ({columns});
    """
    print(f"Creating table: {table_name}")
    cur.execute(create_table_query)
    
    # Now, copy data from the stage into the table
    copy_into_query = f"""
        COPY INTO {table_name}
        FROM '@{STAGE_NAME}/{file}'
        FILE_FORMAT = (FORMAT_NAME = '{FILE_FORMAT}')
        ON_ERROR = 'skip_file';
    """
    print(f"Copying data into table: {table_name}")
    cur.execute(copy_into_query)

print("✅ All tables created and data loaded successfully!")
