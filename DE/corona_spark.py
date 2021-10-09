from pyspark.conf import SparkConf 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
import pyspark
import pyspark.sql.functions as f 

import json

from pymongo import MongoClient
from datetime import datetime

# pymongo connect
client = MongoClient('localhost',27017) # mongodb 27017 port
db = client.ojo_db

spark = SparkSession.builder.appName("example-pyspark-read-and-write").getOrCreate()

nowtime = datetime.today().strftime('%Y-%m-%d')

disp = spark.read.parquet(f"hdfs://localhost:9000/data/corona/coronaAPI_{nowtime}")
disp_st = spark.read.parquet(f"hdfs://localhost:9000/data/corona/coronaStage_{nowtime}")

def corona_processing():
    # spark to pandas processing
    df = disp.select('날짜','area','확진자수')
    df = df.withColumn('date',f.to_date(df['날짜']))
    df.date.cast(StringType())
    df = df.drop('날짜')
    df = df.withColumnRenamed("date", "날짜")
    global disp_st
    disp_st = disp_st.drop('__index_level_0__')
    disp_st = disp_st.withColumnRenamed("Stage", "거리두기단계")
    df_corona = df.join(disp_st, on=['Area'], how='left_outer')
    df_corona = df_corona.withColumnRenamed("area", "지역")
    df_corona = df_corona.withColumnRenamed("Description", "상세내용")

    new_df = df_corona.toJSON().map(lambda x: json.loads(x)).collect()
    for i in new_df:
        db.corona.insert_one(i)

corona_processing()