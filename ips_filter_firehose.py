import json
import boto3
import base64


def lambda_handler(event, context):
    dynamo_db = boto3.resource('dynamodb')
    firehose = boto3.client('firehose')
    table = dynamo_db.Table('mvlajkovic-suspicious-ips-cf')
    actual_items = []
    sample_record = None
    for item in event['Records']:
        record = json.loads(base64.b64decode(item['kinesis']["data"]))
        sample_record = record
        is_suspicious = table.get_item(Key={'user_ip': record['user_ip']})
        if 'Item' not in is_suspicious:
            output_record = {
                'Data': json.dumps(record) + '\n'
            }
            actual_items.append(output_record)

    if 'review_text' in sample_record and len(actual_items) > 0:
        response = firehose.put_record_batch(
            DeliveryStreamName='mvlajkovic-reviews-firehose-cf',
            Records=actual_items)
    elif len(actual_items) > 0:
        response = firehose.put_record_batch(
            DeliveryStreamName='mvlajkovic-views-firehose-cf',
            Records=actual_items
        )
    else:
        return None

    return response
