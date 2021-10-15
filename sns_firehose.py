import boto3
import json
import base64
import os


def lambda_handler(event, context):
    sns = boto3.client('sns')
    threshold = 2
    for item in event['records']:
        record = json.loads(base64.b64decode(item['kinesis']["data"]))
        print(record)
        if record['items_count'] > threshold:
            sns.publish(
                TopicArn=os.environ['SnsArn'],
                Subject=f'Notification for item {record["item_id"]}',
                Message=f'Item {record["item_id"]} is popular!'
            )
