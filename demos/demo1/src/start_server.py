# start_processing

import os
import sys
import process
import datetime

import ConfigParser

import logging
import logging.config

import time
import worker.worker_status

def server_just_built(conf_filename):
    parser = ConfigParser.SafeConfigParser()
    parser.read(conf_filename)
    log_name = parser.get('handler_fileHandler','args').split("'")[1]

    # if the log file does not exist then the box has just become acitve

    if os.path.isfile(log_name):
        return False
    else:
        return True


def main():
    return # ----------------------------------------------------------------

    print '- process --------'

    for i in range(20):
        logger.info(i)
        print i
        try:
            process.processSinglePrice()
        except Exception, e:
            logger.exception('ERROR')
        time.sleep(5)


if __name__ == '__main__':
    filename = r'./ini/logging.conf'
    if not os.path.exists(filename):
        filename = r'./src/ini_default/logging.conf'
        if not os.path.exists(filename):
            print 'No logging file %s' %filename
            sys.exit(2)

    sjb = server_just_built(filename)

    hostname = os.uname()[1]

    logging.config.fileConfig(filename)
    logger = logging.getLogger('startup')
    logger.info('startup on (%s)' %hostname)
    logger.info('server just built (%s)' %sjb)

    if sjb:
        msg = 'wait for hostname to change from (%s)' %(hostname)
        logger.info(msg)

        for i in range(5):
             time.sleep(1)
             if hostname != os.uname()[1]:
                hostname = os.uname()[1]

                msg = 'hostname has changed to (%s)' %(hostname)
                logger.info(msg)
                break

        msg = 'new hostname (%s)' %(hostname)
        logger.info(msg)

        logger.info('Update WorkerStatus to standby ...')
        worker.worker_status.setWorkerStandby(hostname)
        logger.info('Worker set to standby')

        logger.info('start')

    main()
    print 'Done'
