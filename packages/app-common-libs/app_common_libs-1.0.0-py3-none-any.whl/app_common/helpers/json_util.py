import json
import re
from datetime import datetime
from decimal import Decimal

import six


def object_hook(dct):
    """ DynamoDB object hook to return python values """
    try:
        # First - Try to parse the dct as DynamoDB parsed
        if 'BOOL' in dct:
            return dct['BOOL']
        if 'S' in dct:
            val = dct['S']
            return str(val)
        if 'SS' in dct:
            return list(dct['SS'])
        if 'N' in dct:
            if re.match("^-?\d+?\.\d+?$", dct['N']) is not None:
                return float(dct['N'])
            else:
                return int(dct['N'])
        if 'B' in dct:
            return str(dct['B'])
        if 'NS' in dct:
            return set(dct['NS'])
        if 'BS' in dct:
            return set(dct['BS'])
        if 'M' in dct:
            return dct['M']
        if 'L' in dct:
            return dct['L']
        if 'NULL' in dct and dct['NULL'] is True:
            return None
    except:
        return dct
    # In a Case of returning a regular python dict
    return return_regular_python(dct)


def return_regular_python(dct):
    for key, val in six.iteritems(dct):
        if isinstance(val, six.string_types):
            try:
                dct[key] = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')
            except:
                # This is a regular Basestring object
                pass
        if isinstance(val, Decimal):
            if val % 1 > 0:
                dct[key] = float(val)
            else:
                dct[key] = int(val)
    return dct


def parse(s):
    """ Loads DynamoDB json format to a python dict.
    """
    if not isinstance(s, six.string_types):
        s = json.dumps(s)
    return json.loads(s, object_hook=object_hook)
