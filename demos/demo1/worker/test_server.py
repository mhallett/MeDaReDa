# test_server.py

import server

import unittest
import mock

import logging
import logging.config

#logger_conf_file = r'../src/ini_default/logging.conf'
#logging.config.fileConfig( logger_conf_file)

class TestServer(unittest.TestCase):

    def test1(self):
        medareda_ini_values = server.get_ini_values()
        print medareda_ini_values

if __name__ == '__main__':
    unittest.main()
