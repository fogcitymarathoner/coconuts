__author__ = 'marc'

import unittest
from lib import module_exists

class CocoModuleImportTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_imports(self):
        """
        test_imports - makes sure modules will load
        """
        module_list = [
            'Data',
            'DataArray',
            'lib',
            'settings',
            'utils.build_cache'
        ]
        for mod in module_list:
            self.assertTrue(module_exists(mod))
