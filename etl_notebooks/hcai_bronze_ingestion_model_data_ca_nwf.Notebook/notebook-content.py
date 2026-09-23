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

# Data: Modeling Data for California's Nursing Workforce
# Homepage URL: https://hcai.ca.gov/workforce-capacity/workforce-data/
# Contact email: workforcedata@hcai.ca.gov
# Temporal Coverage: Current data as of 2022, model projections 2023-2033
# Frequency: Annually
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

url = f'https://data.chhs.ca.gov/dataset/2c3fd561-a428-444f-8a77-d7987d66bdf4/resource/6cbb8a31-8629-4269-821b-81334ceecde0/download/modeling-data-for-californias-nursing-workforce.xlsx'

table_name = "dbo.dm_model_data_ca_nwf"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Download data

response = requests.get(url)
response.raise_for_status()  # Fail early if the download doesn't succeed

pdf = pd.read_excel(BytesIO(response.content), sheet_name=0)
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
