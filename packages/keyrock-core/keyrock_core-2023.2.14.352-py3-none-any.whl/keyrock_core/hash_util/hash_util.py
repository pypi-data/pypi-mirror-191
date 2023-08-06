import base64
import hashlib
import json
import re

from .. import json_util


def get_str_hash(s, consider_whitespace=False):
    if not consider_whitespace:
        # \s for "any whitespace"
        s = s.replace('\\n', ' ')
        s = re.sub('\s+', ' ', s)
        s = re.sub('\s+', ' ', s)
        s = s.replace('" ', '"').replace(' "', '"')
    h = hashlib.md5()
    h.update(s.encode('utf8'))
    str_hash = h.hexdigest()
    return str_hash


def get_dict_hash(d):
    if d is None:
        d = {}
    s = json_util.dict_to_sorted(d)
    str_val = json.dumps(s, cls=json_util.CustomEncoder)
    str_hash = get_str_hash(str_val)
    return str_hash
