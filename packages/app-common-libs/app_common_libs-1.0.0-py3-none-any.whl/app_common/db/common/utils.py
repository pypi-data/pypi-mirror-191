import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# 1428440
def seconds_to_hm(d):
    if d:
        d = int(d)
        h = d // 3600
        m = d % 3600 // 60
        h_display = h > 0 and f'{h}h ' or ''
        m_display = m > 0 and f'{m}m' or ''
        return f'{h_display}  {m_display}'
    return ''
