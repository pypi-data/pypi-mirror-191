import logging
logger = logging.getLogger(__name__)

import re


def repl_last(s, sub, repl):
    pattern = sub + '(?!.*' + sub + ')'
    result = re.sub(pattern, repl, s, flags=re.DOTALL)
    return result


def strip_limit(query_str):
    if 'limit' not in query_str.lower():
        return query_str

    sub = '\s*LIMIT\s+.*'
    return repl_last(query_str, sub, '')


def set_limit(query_str, limit):
    query_str = strip_limit(query_str)
    query_str += f' LIMIT {limit}'
    return query_str