import json

from app_common.aws.dynamoDB import dynamo_scan
from app_common.db.base import BaseModel
from app_common.db.common import DecimalEncoder

MAX_PAGE_SIZE = 500


def dump_dynamo_data(model: BaseModel, table_name: str, parser_map: dict, next_token: str = None):
    """
    Function scan value from dynamo db table and insert th result in sql
    :param model: SQL Base model which will handle the bulk insertion
    :param table_name: Name of dynamo db table
    :param parser_map: The Sql table key map with dynamo db and parsing function
    :param next_token: Used in case of paginated call
    """
    scan_result = dynamo_scan(table_name, next_token, MAX_PAGE_SIZE)
    rows = []
    for item in scan_result.get('Items', []):
        item = json.loads(json.dumps(item, cls=DecimalEncoder))
        data = {}
        for key, mappings in parser_map.items():
            mapped_key = mappings[0]
            parser_function = mappings[1]
            try:
                data[key] = parser_function(
                    item=item,
                    current_state=data,
                    keys=mapped_key
                )
            except Exception as ex:
                print(f'Parsing exception for {key} with item {item}')
                raise ex
        rows.append(data)
    model.bulk_insert_dict(rows)
    next_token = scan_result.get('LastEvaluatedKey')
    if next_token:
        dump_dynamo_data(model, table_name, parser_map, next_token)
    else:
        print(f'DB dump for table {model} is completed')


def get_value(mapped_key, item):
    if isinstance(mapped_key, list):
        return [item.get(key) for key in mapped_key]
    return item.get(mapped_key)
