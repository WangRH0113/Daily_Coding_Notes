# read_delimited_to_parquet.py
# Simple Databricks script: read CSV/TXT, auto-detect delimiter, add metadata, write Parquet

import re
from pyspark.sql import SparkSession, functions as F

# Filename: CustomerAbbr_WRID_JobDate[_append|_monitor].ext
FILE_RX = r"^(?P<abbr>[A-Za-z0-9]+)_WR(?P<wrid>\d+)_(?P<jobdate>\d{8})(?P<tag>_append|_monitor)?\.(?P<ext>csv|txt)$"

def sniff_delimiter(line, candidates=[",","|",";","\t"]):
    counts = {c: line.count(c) for c in candidates}
    return max(counts, key=counts.get) if line else ","

def main(base, glob="**/*.*", out_parquet=None):
    spark = SparkSession.builder.getOrCreate()
    glob_path = f"{base}/{glob}"
    
    # sniff delimiter from a sample line
    sample = spark.read.text(glob_path).limit(1).collect()
    delimiter = sniff_delimiter(sample[0]["value"]) if sample else ","
    
    df = (spark.read
            .option("header", "true")
            .option("delimiter", delimiter)
            .csv(glob_path))

    df.show(5, truncate=False)
    
    if out_parquet:
        (df.write.mode("append")
           .parquet(out_parquet))

# Example (in Databricks notebook):
# main("abfss://<container>@<account>.dfs.core.windows.net/path/to/LDC",
#      out_parquet="abfss://<container>@<account>.dfs.core.windows.net/bronze/ldc_parquet")
