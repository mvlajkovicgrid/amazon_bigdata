from pyspark.sql import functions as F
import boto3
import json
import os
import base64
from pyspark.sql.session import SparkSession
import time
import sys

table_name = 'mvlajkovic-ip'

bucket = sys.argv[1]
key = sys.argv[2]

path = 's3://' + bucket + '/' + key
print(path)

dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table(table_name)

spark = SparkSession.builder.getOrCreate()

def writeToDynamo(row, table=table):
    table.put_item(Item={'user_ip': row['user_ip']})

df = spark.read.json(path)

df = df.groupBy('user_ip', 'ts')\
        .count()\
        .groupBy('user_ip')\
        .agg(F.avg(F.col('count')).alias('avg'))\
        .where(F.col('avg') > 5)\
        .select('user_ip')

for row in df.collect():
    writeToDynamo(row)

df.show()