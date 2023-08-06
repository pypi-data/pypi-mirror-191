import logging
import os
import yaml
import json

from .. import json_util

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ignore_key_list = ['import']


def load(filepath):
    logger.debug('Load config: {}'.format(filepath))

    root_folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    config_dict = _load_file(root_folder, filename)
    config_dict = _resolve_inheritance(config_dict, config_dict)

    return config_dict


def _load_file(dirname, filename):
    logger.debug('load file: {} {}'.format(dirname, filename))

    file_ext = os.path.splitext(filename)[1]
    filepath = os.path.join(dirname, filename)

    final_dict = {}

    if file_ext in ['.yml', '.yaml']:
        config_dict = _load_yml(filepath)
    elif file_ext in ['.js', '.json']:
        config_dict = _load_json(filepath)
    else:
        logger.error('unrecognized file type: {}'.format(filename))
        return None

    # Assign dot-separated keys to the appropriate nodes
    config_dict = _resolve_dot_values(config_dict)

    if config_dict is not None:
        import_list = config_dict.get('import', [])
        for import_filename in import_list:
            logger.debug('import: {}'.format(import_filename))
            import_dict = _load_file(dirname, import_filename)
            #_merge_config(final_dict, import_dict)
            json_util.deep_update(final_dict, import_dict, ignore_key_list)

    #_merge_config(final_dict, config_dict)
    json_util.deep_update(final_dict, config_dict, ignore_key_list)

    return final_dict


def _load_yml(filepath):
    try:
        with open(filepath) as file:
            file_text = file.read()
            return yaml.load(file_text, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error(e)
        return {}


def _load_json(filepath):
    try:
        with open(filepath) as file:
            file_text = file.read()
            return json.loads(file_text)
    except Exception as e:
        logger.error(e)
        return {}


# def _merge_config(final_dict, layer_dict):
#     if layer_dict is None:
#         return

#     for key, layer_val in layer_dict.items():
#         if key != 'import':
#             current_val = final_dict.get(key)
#             if current_val is None:
#                 final_dict[key] = layer_val
#             elif isinstance(current_val, dict):
#                 if isinstance(layer_val, dict):
#                     _merge_config(current_val, layer_val)
#                 else:
#                     logger.warning('layer value overwrites dict')
#                     final_dict[key] = layer_val
#             else:
#                 final_dict[key] = layer_val


def _resolve_inheritance(root_node, node):
    if node is None:
        return None

    if isinstance(node, dict):
        final_node = {}
        if 'inherit' in node:
            # Load inherited base values first
            for abs_path in node['inherit']:
                inherit_node = _find_node(root_node, abs_path)
                #_merge_config(final_node, inherit_node)
                json.util.deep_update(final_node, inherit_node, ignore_key_list)

            # Copy the remaining values
            for key, val in node.items():
                if key != 'inherit':
                    final_node[key] = _resolve_inheritance(root_node, val)

            return final_node

    if isinstance(node, list):
        final_node = []
        for val in node:
            final_node.append(_resolve_inheritance(root_node, val))

        return final_node

    return node


def _resolve_dot_values(node):
    if node is None:
        return None

    if isinstance(node, dict):
        final_node = {}
        for key, val in node.items():
            final_val = _resolve_dot_values(val)
            _assign_val_to_node(final_node, key, final_val)
        return final_node
    elif isinstance(node, list):
        final_node = []
        for val in node:
            final_node.append(_resolve_dot_values(val))
        return final_node
    else:
        return node


def _find_node(search_node, abs_path):
    keys = abs_path.split('.')
    node = search_node
    for key in keys:
        node = node.get(key)
        if node is None:
            return None
    return node


def _assign_val_to_node(search_node, rel_path, val):
    node = search_node

    keys = rel_path.split('.')
    last_key = keys.pop()
    for key in keys:
        node = node.setdefault(key, {})
        if not isinstance(node, dict):
            raise Exception(f'node already has non-dict value: {key} of {rel_path}')

    if last_key not in node:
        # Nothing to merge
        node[last_key] = val
    else:
        current_val = node[last_key]
        if isinstance(current_val, dict):
            #_merge_config(current_val, val)
            json_util.deep_update(current_val, val, ignore_key_list)
        elif isinstance(current_val, list):
            raise NotImplementedError()
        else:
            node[last_key] = val
