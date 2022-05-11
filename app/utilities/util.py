import json
import decimal
import pandas as pd
from decimal import Decimal
import time


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):  #<---resolving sets as lists
            return list(o)
        return super(DecimalEncoder, self).default(o)

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

'''def convert_json_to_csv(json_string):
    
    dic_flattened = [flatten(d) for d in json_string]
    df = pd.DataFrame(dic_flattened)
    print(df.columns)
    i = df.to_csv('sample1.csv')
    return i

def upload_to_s3(file_name, bucket, key):
    s3 = boto3.resource('s3')
    status = s3.meta.client.upload_file('sample1.csv', 
    'unorganizedbucket-qa-961043014301-us-east-1', 
    'appformdata.csv')
    return status
'''

def prepare_success_response(app_form_id, status_code, body):

    return {
        "statusCode": status_code,
        "body": {
            'responseCode': '000',
            'timestamp': round(time.time() * 1000),
            'appFormId': app_form_id,
            'error': {},
            'responseBody': body
        }
    }

def prepare_failure_response(app_form_id, status_code, error_message, body=None):

    return {
        "statusCode": status_code,
        "body": {
            'responseCode': '101',
            'timestamp': round(time.time() * 1000),
            'appFormId': app_form_id,
            'error': {
                'errorMessage': error_message,
                'errorBody': body
            },
            'responseBody': {}
        }
    }