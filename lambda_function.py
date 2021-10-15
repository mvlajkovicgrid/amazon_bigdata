import json
import boto3
import os

client = boto3.client('emr')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(key)
    
    response = client.run_job_flow(
        Name= "EMR_run",
        LogUri= 's3://' + "mvlajkoviclogsanddata" + '/emr/logs',
        Instances={
            'Ec2KeyName':"m4.large",
            'MasterInstanceType': "m4.large",
            'SlaveInstanceType': "m4.large",
            'InstanceCount': 1,
            'TerminationProtected': False,
            'Ec2SubnetId': "subnet-7d6e3543",
            'KeepJobFlowAliveWhenNoSteps': False
        },
        Applications = [ {'Name': 'Spark'} ],
        VisibleToAllUsers=True,
        JobFlowRole = "EMR_EC2_DefaultRole",
        ServiceRole = "EMR_DefaultRole",
        ReleaseLabel = "emr-5.30.1",
        BootstrapActions = [{
            'Name': 'install boto3',
            'ScriptBootstrapAction': {
                'Path': 's3://' + "mvlajkovicfirstprojecttry" + '/bootstrap_script.sh'
            }
        }],
        Tags = [{
            'Key': 'owner',
            'Value': "neko"
        }],

        Steps=[
            {
                'Name': 'fraud-detection',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': [
                            'spark-submit',
                            's3://' + "mvlajkovicfirstprojecttry" + '/fraud_detection.py',
                            bucket,
                            key
                        ]
                }
            }
        ]
    )