import logging
logger = logging.getLogger(__name__)

import json
import collections


def load_safe(json_str):
    try:
        return json.loads(json_str)
    except:
        return json_str


def dict_to_sorted(d):
    if d is None:
        return None

    if not isinstance(d, dict):
        return d

    s = collections.OrderedDict(sorted(d.items()))
    for key, val in s.items():
        if isinstance(val, dict):
            s[key] = dict_to_sorted(val)

    return s


def only_update_existing(base_dict, new_dict):
    for key, val in base_dict.items():
        # If key isn't in new_dict, keep the old val
        base_dict[key] = new_dict.get(key, val)
    return base_dict


def deep_update(final_dict, layer_dict, ignore_key_list=None):
    if layer_dict is None:
        return final_dict

    for key, layer_val in layer_dict.items():
        if not ignore_key_list is None and key in ignore_key_list:
            continue

        if key not in final_dict:
            final_dict[key] = layer_val
            continue

        current_val = final_dict[key]
        if isinstance(current_val, dict):
            if isinstance(layer_val, dict):
                deep_update(current_val, layer_val, ignore_key_list)
            else:
                logger.warning('layer value overwrites dict')
                final_dict[key] = layer_val
        else:
            final_dict[key] = layer_val

    return final_dict


def delta(dict_from, dict_to):
    patch = {}

    for key, val in dict_to.items():
        if key not in dict_from:
            patch[key] = val
        elif isinstance(val, dict):
            patch[key] = delta(val, dict_from[key])
        elif isinstance(val, list):
            patch[key] = val
        elif val != dict_from[key]:
            patch[key] = val

    return patch


def get_node(d, path_str, default_val=None):
    path_array = path_str.split('.')
    node = d
    for branch in path_array:
        if isinstance(node, dict):
            node = node.get(branch)
        elif isinstance(node, list):
            node = node[int(branch)]
        else:
            return default_val
    return node


def get_path_value(d, path_str, default_val=None):
    return get_node(d, path_str, default_val)


def set_path_value(node, path_str, val):
    #print('SET PATH VALUE', node['id'], path_str, val)
    path_array = path_str.split('.')
    last_branch = path_array.pop()
    for branch in path_array:
        if isinstance(node, dict):
            node = node.setdefault(branch, {})
        elif isinstance(node, list):
            node = node[int(branch)]
        else:
            raise Exception('set_path_value: existing search node is not a dict or list')

    if isinstance(node, dict):
        node[last_branch] = val
    elif isinstance(node, list):
        node[int(last_branch)] = val
    else:
        raise Exception('set_path_value: penultimate node is not a dict or list')

    return node


def prune_sub_dicts(node):
    if node is None or not isinstance(node, dict):
        return node
    for key, val in node.items():
        node[key] = omit_dicts(val)


def omit_dicts(node):
    if node is None or not isinstance(node, dict):
        return node
    pruned_node = {}
    for key, val in node.items():
        if isinstance(val, dict):
            pruned_node[key] = '...'
        else:
            pruned_node[key] = val
    return pruned_node


def find_paths_with_value(search_val, src_data, key_filter_list=None, current_path=None, depth=0, current_key=None):
    # Find all paths with this value as the RHS
    # If key_filter_list is present, only include keys from the list
    if not src_data:
        return []

    max_depth = 10
    if depth > max_depth:
        logger.warning('find_paths_with_value: max depth reached:', max_depth)
        return []
    depth += 1

    if current_path is None:
        current_path = ''

    if current_key is None:
        current_key = current_path

    if isinstance(src_data, dict):
        path_list = []
        for key, val in src_data.items():
            sub_path = '{0}.{1}'.format(current_path, key)
            sub_path_list = find_paths_with_value(
                search_val, src_data=val, key_filter_list=key_filter_list, current_path=sub_path, depth=depth, current_key=key)
            path_list.extend(sub_path_list)
        return path_list
    elif isinstance(src_data, list):
        path_list = []
        for i, val in enumerate(src_data):
            sub_path = '{0}.{1}'.format(current_path, i)
            sub_path_list = find_paths_with_value(
                search_val, src_data=val, key_filter_list=key_filter_list, current_path=sub_path, depth=depth, current_key=i)
            path_list.extend(sub_path_list)
        return path_list
    elif src_data == search_val:
        if key_filter_list is not None and current_key in key_filter_list:
            return [current_path]

    return []


def find_paths_with_key(search_key, src_data, current_path=None, depth=0):
    if not src_data:
        return []

    max_depth = 10
    if depth > max_depth:
        logger.warning('find_paths_with_key: max depth reached:', max_depth)
        return []
    depth += 1

    path_list = []
    if isinstance(src_data, dict):
        for key, val in src_data.items():
            if current_path is None:
                sub_path = key
            else:
                sub_path = '{0}.{1}'.format(current_path, key)

            if key == search_key:
                path_list.append(sub_path)
            # Continue searching recusrively for nested keys
            sub_path_list = find_paths_with_key(
                search_key, src_data=val, current_path=sub_path, depth=depth)
            path_list.extend(sub_path_list)
    elif isinstance(src_data, list):
        for i, val in enumerate(src_data):
            if current_path is None:
                sub_path = key
            else:
                sub_path = '{0}.{1}'.format(current_path, i)

            # Continue searching recusrively for nested keys
            sub_path_list = find_paths_with_key(
                search_key, src_data=val, current_path=sub_path, depth=depth)
            path_list.extend(sub_path_list)
    return path_list
