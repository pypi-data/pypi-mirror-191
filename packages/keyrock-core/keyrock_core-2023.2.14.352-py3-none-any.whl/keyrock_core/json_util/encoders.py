import json
import datetime
import decimal
import typing
import io
import math

import logging
logger = logging.getLogger(__name__)

# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return str(obj)
#         elif isinstance(obj, datetime.date):
#             return str(obj)
#         elif isinstance(obj, bytes):
#             return obj.decode("utf-8", "replace")
#         return json.JSONEncoder.default(self, obj)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, datetime.date):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return (str(o) for o in [obj])
        elif isinstance(obj, typing.Generator):
            # @hack: deal with aggregate-function Snowflake result data
            list_conv = [o for o in obj]
            if len(list_conv) == 1:
                return list_conv[0]
            else:
                return json.dumps(list_conv)
        elif isinstance(obj, bytes):
            return obj.decode("utf-8", "replace")
        elif isinstance(obj, memoryview):
            #return obj.tobytes().decode("utf-8", "replace")
            return '[BINARY DATA]'
        return json.JSONEncoder.default(self, obj)
        #return json.dumps(obj, allow_nan=False)
