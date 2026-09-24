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

 # A simple etl flow from bronze to silver for primary care shortage areas


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import Libraries
from pyspark.sql import functions as F

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parameters

bronze_table = "dbo.dm_primary_care_shortage_areas"
silver_table = "silver.dm_primary_care_shortage_areas"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read table

df_bronze = spark.table(bronze_table)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add metadata

df_silver = (
    df_bronze
    .withColumn("_etl_processed_at", F.current_timestamp())
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load table

(
    df_silver
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_table)
)


print(f"Successfully processed {df_silver.count()} records.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
