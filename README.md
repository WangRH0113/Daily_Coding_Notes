# Daily Coding Notes

A collection of utilities and notes for data access patterns across Azure cloud services, including AzureML, Databricks, and Azure Data Lake Storage.

## Overview

This project aims to document and provide practical examples for accessing and transforming data across various Azure cloud services. It includes utilities for working with different file formats (CSV, Parquet, TXT) and demonstrates best practices for data engineering workflows.

## Features

- **Multi-format Support**: Handle CSV, TXT, and Parquet file formats
- **Auto-delimiter Detection**: Automatically detect delimiters in delimited text files
- **Azure Integration**: Seamless integration with Azure Data Lake Storage (ADLS Gen2)
- **Databricks Optimized**: Scripts designed to run efficiently on Databricks clusters
- **Metadata Preservation**: Maintain file metadata during transformations

## Contents

### Scripts

- **`read_delimited_to_parquet.py`**: A Databricks script that reads CSV/TXT files, auto-detects delimiters, and writes to Parquet format

## Installation

### Prerequisites

- Python 3.7+
- Apache Spark 3.x (for Databricks environment)
- PySpark library
- Access to Azure Data Lake Storage (for production use)

### Setup

For local development with PySpark:

```bash
pip install pyspark
```

For Databricks, no additional installation is required as PySpark is pre-installed.

## Usage

### Reading Delimited Files and Converting to Parquet

The `read_delimited_to_parquet.py` script provides a simple way to read delimited files (CSV/TXT) and convert them to Parquet format with automatic delimiter detection.

**Basic Usage in Databricks Notebook:**

```python
# Import the main function
from read_delimited_to_parquet import main

# Process files from Azure Data Lake Storage
main(
    base="abfss://<container>@<account>.dfs.core.windows.net/path/to/data",
    glob="**/*.*",
    out_parquet="abfss://<container>@<account>.dfs.core.windows.net/bronze/output_parquet"
)
```

**Parameters:**

- `base`: Base path to your data source (supports ADLS paths)
- `glob`: Pattern to match files (default: `**/*.*`)
- `out_parquet`: Output path for Parquet files (optional)

**Supported Delimiters:**

The script automatically detects the following delimiters:
- Comma (`,`)
- Pipe (`|`)
- Semicolon (`;`)
- Tab (`\t`)

**File Naming Convention:**

The script is optimized for files following this pattern:
```
CustomerAbbr_WRID_JobDate[_append|_monitor].ext
```

Example: `ACME_WR12345_20231030_append.csv`

### Example Workflow

1. **Upload CSV files** to Azure Data Lake Storage
2. **Run the script** in a Databricks notebook
3. **Output** is written to the specified Parquet location
4. **Verify** the data using Spark DataFrame operations

```python
# Read the resulting Parquet files
df = spark.read.parquet("abfss://<container>@<account>.dfs.core.windows.net/bronze/output_parquet")
df.show(10)
```

## Azure Services Integration

This project demonstrates integration with the following Azure services:

- **Azure Data Lake Storage Gen2**: Primary storage for input and output files
- **Azure Databricks**: Execution environment for Spark jobs
- **Azure Machine Learning**: Data pipeline integration (documentation in progress)

## Contributing

Contributions are welcome! If you have additional utilities or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-utility`)
3. Commit your changes (`git commit -am 'Add new utility'`)
4. Push to the branch (`git push origin feature/new-utility`)
5. Open a Pull Request

## Best Practices

- Always specify the correct Azure storage account and container in your paths
- Use managed identities or service principals for authentication
- Test scripts with small datasets before processing large files
- Monitor Spark job metrics in Databricks for performance optimization
- Use Parquet format for better compression and query performance

## License

This project is available for educational and reference purposes.

## Acknowledgments

- Built for Azure cloud data engineering workflows
- Optimized for Databricks Spark environments
