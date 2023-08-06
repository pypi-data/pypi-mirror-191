import json

import logging
logger = logging.getLogger(__name__)


def diff(obj_from, obj_to, explicit_group_list=None, ignore_group_list=None, group_key=None):
    ''' explicit_group_list:
            if None:
                always delete missing items
            if not None:
                only delete items missing from groups specified in the list (by group key)
                otherwise consider them as unchanged
    '''
    if isinstance(obj_from, dict) and isinstance(obj_to, dict):
        return diff_dict(obj_from, obj_to, explicit_group_list, ignore_group_list, group_key)

    if isinstance(obj_from, list) and isinstance(obj_to, list):
        return diff_list(obj_from, obj_to, explicit_group_list, ignore_group_list, group_key)

    if str(obj_from) != str(obj_to):
        return {
            'op': 'mod',
            'val_from': obj_from,
            'val': obj_to,
        }

    return {
        'op': None,
        'val': obj_from,
    }


def diff_dict(dict_from, dict_to, explicit_group_list, ignore_group_list, group_key):
    result = {
        'op': 'dict',
        'diff': {},
    }

    has_sub_diff = False

    # Find the additions
    for key, val in dict_to.items():
        if ignore_group_list is not None and key in ignore_group_list:
            pass
        elif key not in dict_from:
            has_sub_diff = True
            result['diff'][key] = {
                'op': 'add',
                'val': val,
            }

    # Find the subtractions
    if explicit_group_list is None or group_key in explicit_group_list:
        for key, val in dict_from.items():
            if ignore_group_list is not None and key in ignore_group_list:
                pass
            elif key not in dict_to:
                has_sub_diff = True
                result['diff'][key] = {
                    'op': 'del',
                    'val_from': val,
                }

    # Find the changes
    for key, val_from in dict_from.items():
        if ignore_group_list is not None and key in ignore_group_list:
            pass
        elif key in dict_to:
            val_to = dict_to[key]
            sub_result = diff(val_from, val_to, explicit_group_list, ignore_group_list, key)
            result['diff'][key] = sub_result
            if sub_result['op'] is not None:
                has_sub_diff = True

    if not has_sub_diff:
        return {
            'op': None,
            'val': dict_from,
        }

    return result


def diff_list(list_from, list_to, explicit_group_list, ignore_group_list, group_key):
    mod_result = {
        'op': 'mod',
        'val_from': list_from,
        'val': list_to,
    }

    if len(list_from) != len(list_to):
        return mod_result

    for v in list_from:
        assert(not isinstance(v, dict)), 'dict elements not allowed in list'
        assert(not isinstance(v, list)), 'list elements not allowed in list'
        if v not in list_to:
            return mod_result

    for v in list_to:
        assert(not isinstance(v, dict)), 'dict elements not allowed in list'
        assert(not isinstance(v, list)), 'list elements not allowed in list'
        if v not in list_from:
            return mod_result

    return {
        'op': None,
        'val': list_from,
    }


def strip_unchanged(diff_node):
    op = diff_node['op']
    if op == 'dict':
        return_val = {'op': 'dict', 'dict': {}}
        for item_key, item_node in diff_node['diff'].items():
            if item_node['op'] is None:
                pass
            elif item_node['op'] == 'dict':
                return_val['dict'][item_key] = strip_unchanged(item_node)
            else:
                return_val['dict'][item_key] = item_node
        return return_val
    elif op is None:
        return None
    else:
        return diff_node


def assemble_node_data(diff_node):
    op = diff_node['op']
    if op == 'dict':
        pass
    elif op == 'del':
        assert(False), "cannot delete self"
    else:
        return diff_node['val']


def get_property_op(diff_node, prop_key):
    if prop_key in diff_node:
        op = diff_node[prop_key].get('op')
        return op
    return None