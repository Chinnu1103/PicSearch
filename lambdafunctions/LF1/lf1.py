import json
import boto3
import requests
from datetime import datetime
import uuid
import os


# AWS services clients
region = 'us-west-2'
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
opensearch_client = boto3.client('es')

#AWS Credentials
service = 'es'
es_username = os.environ['username']
es_password = os.environ['password']

# OpenSearch configuration
index_name = 'photos'
doc_type = '_doc'
es_endpoint = "search-photos-sre4inqjcx2j6rh44kowdr7ooy.us-west-2.es.amazonaws.com"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        metadata = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        photo_object = response['Body'].read()
        
        rekognition_response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            MaxLabels=10
        )
        
        labels = [label['Name'] for label in rekognition_response['Labels']]
        
        if 'customlabels' in metadata['Metadata']:
            custom_labels = metadata['Metadata']['customlabels'].split(",")
            labels += custom_labels
        
        dt = datetime.strptime(metadata['ResponseMetadata']['HTTPHeaders']['date'], "%a, %d %b %Y %H:%M:%S %Z")
        created_time = dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        document = {
            'objectKey': object_key,
            'bucket': bucket_name,
            'createdTimestamp': created_time,
            'labels': labels
        }

        try:
            response = index_document(document)
            print("Document indexed successfully: ", response)
        except Exception as e:
            print("Document Indexing failed: ", e)

def index_document(document):
    id = str(uuid.uuid4())
    url = f'https://{es_endpoint}/{index_name}/{doc_type}/{id}'
    headers = {'Content-Type': 'application/json'}
    auth = (es_username, es_password)
    response = requests.put(url, auth=auth, headers=headers, data=json.dumps(document))
    return response
