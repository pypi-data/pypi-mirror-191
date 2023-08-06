def extract_values_for_keys(value_objs, keys=()):
    if isinstance(value_objs, list):
        values = []
        keys = keys or value_objs[0].keys()
        for obj in value_objs:
            obj = '\', \''.join([str(obj.get(k, 'NULL')) for k in keys])
            values.append(f'(\'{obj}\')')
        return ',\n'.join(values)
    # If received object is not list type throw an exception
    received_type = type(value_objs).__name__
    expected_type = type([]).__name__
    err_message = f'Unsupported value type objects <{received_type}> required <{expected_type}>'
    print(err_message)
    raise Exception(err_message)
