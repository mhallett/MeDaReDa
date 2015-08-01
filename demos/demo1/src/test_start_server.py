# test_start_server.py

import start_server
import logging
import logging.config
import unittest
import mock
from mock import patch


logger_conf_file = r'./ini_default/logging.conf'
logging.config.fileConfig( logger_conf_file)

#@mock.patch(start_server.server_just_built)
#@mock.patch(start_server.main)

class TestStarstServer(unittest.TestCase):
#log = logging.getLogger('root')
    @mock.patch('start_server.main')
    def test1(self, ssm):
        log = logging.getLogger('test')
        log.info('First Test ------------------------------')

        start_server.main()

    @mock.patch('start_server.server_just_built')
    @mock.patch('worker.worker_status._execute_sql')
    def test2(self,es, mock_sjb):
        mock_sjb.return_value = True
        log = logging.getLogger('test')
        log.info('Second test ----------------------------')
        start_server.main()

    @mock.patch('start_server.server_just_built')
    @mock.patch('worker.worker_status._execute_sql')
    def test3(self,es, sjb):
        sjb.return_value = False
        log = logging.getLogger('test')
        log.info('Third test-------------------------------')
        start_server.main()



unittest.main()
