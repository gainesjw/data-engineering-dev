# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "39f88276-919c-423c-9eb6-a9f7f8756b2a",
# META       "default_lakehouse_name": "lakehouse",
# META       "default_lakehouse_workspace_id": "568ce359-e900-4f84-8b61-154ca0982445",
# META       "known_lakehouses": [
# META         {
# META           "id": "39f88276-919c-423c-9eb6-a9f7f8756b2a"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Web to bronze ingestion

# Sources: data.chhs.ca.gov/

# Data: Primary Care Shortage Areas in California
# Homepage URL: https://hcai.ca.gov/workforce-capacity/workforce-data/
# Contact email: workforcedata@hcai.ca.gov
# Temporal Coverage: Point in Time
# Frequency: Point in Time
# Limitations: Use of this data is subject to the CHHS Terms of Use and any copyright and proprietary notices incorporated in or accompanying the individual files.
# Data last updated: 11/6/2025 (HCAI Stated)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Libraries

import pandas as pd
import requests
from io import BytesIO

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parameters

url = f'https://data.chhs.ca.gov/dataset/061494a3-e8c7-4615-a22f-b2851d44eb09/resource/0ba7c904-2302-400a-ba27-b8e8e5c1ab4a/download/pcsa.csv'

table_name = "dbo.dm_primary_care_shortage_areas"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Download data

response = requests.get(url)
response.raise_for_status()  # Fail early if the download doesn't succeed

pdf = pd.read_csv(BytesIO(response.content))
df = spark.createDataFrame(pdf)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Light cleaning to ingest into lakehouse as a table

# Delta tables do not allow certain characters (e.g., space, %, etc.) in column names.
for c in df.columns:
    new_c = (
        c.strip()
         .replace(" ", "_")
         .replace("%", "pct")
         .replace("(", "")
         .replace(")", "")
         .replace("{", "")
         .replace("}", "")
         .replace(";", "")
         .replace("=", "_")
         .replace("\t", "_")
         .replace("\n", "_")
    )
    if new_c != c:
        df = df.withColumnRenamed(c, new_c)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load data to lakehouse

df.write.mode("overwrite").format("delta").saveAsTable(table_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
