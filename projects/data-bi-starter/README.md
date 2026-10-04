# Data Pipeline & BI Starter

A working Python batch ETL program shares Ops Studio's validation and SQLite transformation code, writes aggregated CSV, and provides Power BI measures and a native Databricks/PySpark Delta merge notebook.

Run from this directory with Python 3.11+:
```sh
python pipeline.py examples/tickets.csv
```
The program writes `data/tickets.sqlite` and `data/summary.csv`. Re-importing updates matching IDs rather than duplicating records. Rejected rows are printed with reasons; exit 2 means some rows were rejected and valid rows were still committed. Its core ETL is covered by Ops Studio tests.

In Power BI Desktop, import the summary CSV as table `Summary`, set numeric types and add the measures from `powerbi/measures.dax` individually. Create cards for totals/open/resolved and a bar chart of priority versus SLA Met Rate. This provides actual importable data and DAX source, not a prebuilt .pbix file. The Ops Studio UI already renders the same analytics without Power BI.

The Databricks notebook requires a Spark runtime supporting `try_to_timestamp`, Delta Lake, a workspace and authorized storage paths. It validates timestamps, rejects duplicate IDs and merges valid rows by ID; invalid rows are displayed. It is an optional platform implementation and has not been executed against Databricks. No workspace or paid cluster has been provisioned.
