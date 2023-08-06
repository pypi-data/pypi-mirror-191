import os

import boto3

API_NAME = os.environ.get('api_name')
region = os.environ.get('region')
DYNAMO_DB = boto3.resource('dynamodb', region_name=region)


def dynamo_scan(table_name, next_token=None, limit=None):
    """
    Sca DynamoDB table and provide the result if next token is available then it wil fetch
    the result for next page
    :param table_name: DynamoDB table name
    :param next_token: next token can be None
    :param limit: maximum item count in single call
    :return: scan result from DynamoDB table
    """
    query_dict = dict()
    table = DYNAMO_DB.Table(f'{API_NAME}-{table_name}')
    if limit:
        query_dict['Limit'] = limit
    if next_token:
        query_dict['ExclusiveStartKey'] = next_token
    print(f'scanning from table({table})')
    scan_result = table.scan(**query_dict)
    return scan_result
