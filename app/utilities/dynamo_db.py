import boto3
import json
from app.utilities.util import DecimalEncoder, prepare_success_response, prepare_failure_response, read_config_file

import os

from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

APPFORM_TABLENAME = read_config_file('dynamodb','tablename')

def get_appform_data(appformid):
    table = dynamodb.Table(APPFORM_TABLENAME)
    print("table : "+APPFORM_TABLENAME)
    response = table.get_item(Key={
    "appFormId": appformid
    })
    if 'Item' in  response:
        raw_res = response['Item']
        return prepare_success_response(appformid, 200, raw_res)
    else:
        return prepare_failure_response(appformid, 424, "AppForm not Found")


def get_all_appform_data(from_date,to_date):
    table = dynamodb.Table(APPFORM_TABLENAME)
    response = table.scan(FilterExpression=Attr('createdAt').gte(from_date) & Attr('createdAt').lt(to_date))
    data = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    dumped_string = json.dumps(data, cls=DecimalEncoder)
 
    return dumped_string

def get_home_page_data(phone_number, sub_id):
    
    items = get_entry_by_phone_number(
        phone_number, sub_id)
    response = None
    #logger.info(items)
    credit_line_cards = []
    loan_cards = None
    count = 1
    if not items:
        credit_line_cards.append(
            prepare_creditline_card('new-application', 0, count))

    for item in items:
        if int(item['status']) < 0:
            rejection_code = None
            rejection_message = None
            if 'rejectionCode' in item:
                rejection_code = item['rejectionCode']
                rejection_message = get_message_for_rejection_code(
                    rejection_code)
            else:
                rejection_code = 'default'
                rejection_message = 'default'

            credit_line_cards.append(prepare_creditline_card(
                'rejected-application', item['state'], count, rejection_code, rejection_message))
        elif int(item['status']) > 0 and "creditLimit" not in item:
            credit_line_cards.append(prepare_creditline_card(
                'application-in-progress', item['state'], count, None, None))
        elif int(item['status']) > 0 and "creditLimit" in item and "currentWithdrawal" not in item:
            credit_line_cards.append(prepare_creditline_card(
                'active-credit-line', item['state'], count, None, None))
        elif int(item['status']) > 0 and "creditLimit" in item and "currentWithdrawal" in item:
            currWithdrawal = item['currentWithdrawal']
            applicant = item['applicant']
            if "withdrawalStatus" in currWithdrawal and currWithdrawal["withdrawalStatus"] == "LOAN_CREATED":
                # for the case of new application with the user with an already existing loan/s
                credit_line_cards.append(prepare_creditline_card(
                    'loans-created', item['state'], count, None, None))
                loan_cards = prepare_loans_card(applicant['pennantCif'])
            elif "withdrawalStatus" in currWithdrawal and currWithdrawal["withdrawalStatus"] != "LOAN_CREATED" or "WITHDRAWAL_CONFIRMED":
                credit_line_cards.append(prepare_creditline_card(
                    'active-credit-line', item['state'], count, None, None))
        count = count+1
    response = prepare_response(credit_line_cards, loan_cards)
    return prepare_success_response(None, 200, response)


def prepare_response(credit_line_cards, loan_cards):
    if loan_cards is not None:
        return {
            'cards': {
                'creditLine': credit_line_cards,
                'loans': loan_cards
            }
        }
    else:
        return {
            'cards': {
                'creditLine': credit_line_cards,
            }
        }


def get_message_for_rejection_code(rejectionCode):
    if rejectionCode == 'CPC_AGE_FAILED' or rejectionCode == 'EMPLOYMENT_VERIFICATION_FAILED' or rejectionCode == 'INITIAL_OFFER_REJECTED' or rejectionCode == 'FINAL_OFFER_REJECTED' or rejectionCode == 'CPC_INCOME_FAILED':
        return 'Sorry, we cannot process your loan currently. You do not match our eligibility criteria.'
    elif rejectionCode == 'CPC_PINCODE_FAILED':
        return 'Sorry, we cannot process your loan as your location is currently unserviceable.'
    elif rejectionCode == 'CPC_SALARYTYPE_FAILED':
        return "Sorry, we are not processing loans to self-employed individuals currently. We'll get in touch with you. But it's not all bad news, you can reapply in 90 days."
    elif rejectionCode == 'PAN_VERIFICATION_FAILED':
        return "Sorry, we cannot process your loan currently. We were unable to verify your PAN."


def prepare_creditline_card(response_type, state, order,  rejection_code, message):
    card = None
    if response_type == 'new-application':
        card = {
            'order': order,
            'type': 'creditLine',
            'state': str(state),
            'title': 'ACTIVATE CREDIT LINE',
            'subtitle': 'Get up to 5 lakhs for 60 months and just pay interest for what you borrow.',
            'buttonText': 'Apply for credit line'
        }
    elif response_type == 'application-in-progress':
        card = {
            'order': order,
            'type': 'creditLine',
            'state': str(state),
            'title': 'ACTIVATE CREDIT LINE',
            'subtitle': 'Get up to 5 lakhs for 60 months and just pay interest for what you borrow.',
            'buttonText': 'Complete Application'
        }
    elif response_type == 'active-credit-line':
        card = {
            'order': order,
            'type': 'creditLine',
            'state': str(state),
            'title': 'CREDIT LINE ACTIVE',
            'subtitle': 'Get up to 5 lakhs for 60 months and just pay interest for what you borrow.',
            'buttonText': 'Withdraw'
        }
    elif response_type == 'rejected-application':
        card = {
            'order': order,
            'type': 'creditLine',
            'state': str(state),
            'title': '',
            'subtitle': 'Oops, your credit line was rejected',
            'buttonText': 'View Application',
            'rejectionCode': rejection_code,
            'rejectionMessage': message
        }
    elif response_type == 'loans-created':
        card = {
            'order': order,
            'type': 'creditLine',
            'state': str(state),
            'title': '',
            'subtitle': '',
            'buttonText': ''
        }
    return card


def prepare_loans_card(cif):
    return {
        'order': 1,
        'type': 'loans',
        'title': 'PERSONAL LOANS',
        'subtitle': 'Check all your loan details here',
        'buttonText': 'View loan details',
        'cif': str(cif)
    }

def get_entry_by_phone_number(phone_number, sub_id):
    table = dynamodb.Table(APPFORM_TABLENAME)
    resp = table.scan(FilterExpression=Attr(
        'applicant.phoneNumber').eq(phone_number))
    items = resp['Items']
    response = []
    for item in items:
        applicant = item["applicant"]
        if 'subId' in applicant and sub_id in applicant["subId"]:
            response.append(item)
    return response