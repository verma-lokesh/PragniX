import json
from datetime import date, datetime
from decimal import Decimal


class NavoraJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def to_json(obj) -> str:
    return json.dumps(obj, cls=NavoraJSONEncoder)
