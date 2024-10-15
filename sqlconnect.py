import psycopg2
from psycopg2 import extras
import pandas as pd
import os
import glob

# 1. Find the most recently modified file in the specified directory
directory = r"C:\Users\Public\Documents\ChargeBreakdowns"
list_of_files = glob.glob(os.path.join(directory, "*.csv"))
latest_file = max(list_of_files, key=os.path.getmtime)

# 2. Read the CSV file
data_frame = pd.read_csv(latest_file, header=None)

#2.5 Convert df to list of tuples
data_to_upsert = [tuple(row) for row in data_frame.itertuples(index=False, name=None)]

# 3. Database connection details
db_params = {
    "user": "postgres",
    "password": "Crystalview2020_",
    "host": "localhost",
    "port": "5432",
    "database": "RM_Reports"
}

# 4. Upsert script
try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Define the upsert query
    upsert_query = """
    INSERT INTO chargebreakdown (propertyheaders, tenant, acc, unit, unittype, rc, lc, bd, cam, h2o, prin, sewer, petfee, elect, trash, wcrd, lint, other, total)
    VALUES %s
    ON CONFLICT (propertyheaders, tenant, acc) DO UPDATE SET
    unit = EXCLUDED.unit,
    unittype = EXCLUDED.unittype,
    rc = EXCLUDED.rc,
    lc = EXCLUDED.lc,
    bd = EXCLUDED.bd,
    cam = EXCLUDED.cam,
    h2o = EXCLUDED.h2o,
    prin = EXCLUDED.prin,
    sewer = EXCLUDED.sewer,
    petfee = EXCLUDED.petfee,
    elect = EXCLUDED.elect,
    trash = EXCLUDED.trash,
    wcrd = EXCLUDED.wcrd,
    lint = EXCLUDED.lint,
    other = EXCLUDED.other,
    total = EXCLUDED.total;
    """

    # Perform the upsert
    extras.execute_values(cursor, upsert_query, data_to_upsert)

    # Commit the transaction
    connection.commit()
    print(f"{cursor.rowcount} Records upserted successfully into table")

except (Exception, psycopg2.Error) as error:
    print("Error in transaction:", error)

finally:
    # Close the connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")