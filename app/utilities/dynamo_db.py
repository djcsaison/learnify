import boto3
import json
from app.utilities.util import DecimalEncoder, prepare_success_response, prepare_failure_response
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

APPFORM_TABLENAME = os.getenv('APPFORM_TABLENAME')

def get_appform_data(appformid):
    table = dynamodb.Table('Privo-AppForm-int')
    response = table.get_item(Key={
    "appFormId": appformid
    })
    if 'Item' in  response:
        raw_res = response['Item']
        return prepare_success_response(appformid, 200, raw_res)
    else:
        return prepare_failure_response(appformid, 424, "AppForm not Found")


def get_all_appform_data(from_date,to_date):
    table = dynamodb.Table('Privo-AppForm-qa')
    response = table.scan(FilterExpression=Attr('createdAt').gte(from_date) & Attr('createdAt').lt(to_date))
    data = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    dumped_string = json.dumps(data, cls=DecimalEncoder)
 
    return dumped_string
