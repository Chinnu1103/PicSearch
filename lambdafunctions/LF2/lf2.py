import json
import uuid
from datetime import datetime
import boto3
import string
import requests
import random
import os

def get_photos(labels):
    if(len(labels) == 0):
        return []
    region = 'us-west-2'
    service = 'es'
    search_url = "https://search-photos-sre4inqjcx2j6rh44kowdr7ooy.us-west-2.es.amazonaws.com"
    search_url = search_url + '/' + "photos" + '/_search'
    
    term_set = [{"term": {"labels": val}} for val in labels]
    
    query_body = {
        "query": {
            "bool": {
                "must": term_set
            }
        }
    }
    
    usr = os.environ['username']
    pwd = os.environ['password']
    auth = (usr, pwd)
    headers = { "Content-Type": "application/json" }
    res = requests.get(search_url, auth=auth, headers=headers, data=json.dumps(query_body))
    
    res = json.loads(res.text)
    print(res)
    
    return res['hits']['hits']

def get_s3_url(bucket, obj):
    return 

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {})
    text = query_params.get('q', None)
    print(text)
    characters = string.ascii_letters + string.digits
    session_id = ''.join(random.choices(characters, k=12))
    
    client = boto3.client('lexv2-runtime')
    response = client.recognize_text(
        botId="K7HUZWYGDK",
        botAliasId="TSTALIASID",
        localeId="en_US",
        sessionId=session_id,
        text=text
    )
    print(response)
    
    slots = response["sessionState"]["intent"]["slots"]
    
    labels = []
    if 'object1' in slots and slots['object1']:
        labels.append(slots['object1']['value']['interpretedValue'])
    if 'object2' in slots and slots['object2']:
        labels.append(slots['object2']['value']['interpretedValue'])
    
    results = []
    try:
        photos = get_photos(labels)
        for item in photos:
            bucket = item["_source"]["bucket"]
            obj = item["_source"]["objectKey"]
            url = f"https://{bucket}.s3.amazonaws.com/{obj}"
            labels = item["_source"]["labels"]
            results.append({
                "url": url,
                "labels": labels
            })
    except Exception as e:
        print(e)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin' : "*",
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({"results": results})
    }
