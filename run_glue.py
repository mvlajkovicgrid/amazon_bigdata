import boto3
import botocore
import os
def lambda_handler(event, context):
    crawler_name = "mv_view_crawler"
    session = boto3.session.Session()
    glue_client = session.client('glue')
    response = glue_client.start_crawler(Name=crawler_name)
    print(response)
    return response