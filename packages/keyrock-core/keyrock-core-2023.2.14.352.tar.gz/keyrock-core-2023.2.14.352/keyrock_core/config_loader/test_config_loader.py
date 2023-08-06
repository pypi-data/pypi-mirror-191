import unittest

import os
import json

from . import *

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logging.getLogger('keyrock_core.config_loader.config_loader').setLevel(logging.DEBUG)


class TestConfigUtil(unittest.TestCase):
    def test_root(self):
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
        
        config = load(os.path.join(ROOT_DIR, 'test_data/example_root.yml'))
        logger.debug(json.dumps(config, indent=2))

        self.assertEquals(config['test_dict']['int_item'], 69)
        self.assertEquals(config['test_dict']['imported_item'], 'from_yaml')
        self.assertEquals(config['test_dict']['dict_item']['imported_item'], 123)
        self.assertEquals(config['test_dict']['js_item'], 'from_json')

        #config = load(os.path.join(ROOT_DIR, 'test_data/bad_example.yml'))
        #print(json.dumps(config, indent=2))
