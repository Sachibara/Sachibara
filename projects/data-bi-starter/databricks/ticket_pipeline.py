# Databricks notebook source
# Configure an authorized input CSV path and a writable Delta output path.
dbutils.widgets.text('input_path','')
dbutils.widgets.text('output_path','')
source=dbutils.widgets.get('input_path');target=dbutils.widgets.get('output_path')
if not source or not target:raise ValueError('Set input_path and output_path.')
from pyspark.sql import functions as F
from delta.tables import DeltaTable
schema='id STRING, priority STRING, opened_at STRING, resolved_at STRING'
raw=spark.read.option('header',True).schema(schema).csv(source)
staged=raw.select(F.trim('id').alias('id'),F.upper(F.trim('priority')).alias('priority'),F.expr('try_to_timestamp(opened_at)').alias('opened_at'),F.expr('try_to_timestamp(resolved_at)').alias('resolved_at'),F.col('resolved_at').alias('resolved_raw'))
valid=(F.col('id').isNotNull() & (F.length('id')>0) & F.col('priority').isin('P1','P2','P3') & F.col('opened_at').isNotNull() & ((F.col('resolved_raw').isNull() | (F.trim('resolved_raw')=='')) | (F.col('resolved_at').isNotNull() & (F.col('resolved_at')>=F.col('opened_at')))))
good=staged.filter(F.coalesce(valid,F.lit(False))).drop('resolved_raw')
bad=staged.filter(~F.coalesce(valid,F.lit(False)))
if good.groupBy('id').count().filter('count > 1').limit(1).count():raise ValueError('Duplicate IDs in import; resolve duplicates before writing.')
if DeltaTable.isDeltaTable(spark,target):
    DeltaTable.forPath(spark,target).alias('t').merge(good.alias('s'),'t.id = s.id').whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
else:good.write.format('delta').mode('errorifexists').save(target)
display(bad)
display(spark.read.format('delta').load(target).groupBy('priority').count())
