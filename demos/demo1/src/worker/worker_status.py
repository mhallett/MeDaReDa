# worker_status.py

import time
import datetime
import socket
import medareda_lib
import logging

#f_logger = logging.getLogger(__name__)
f_logger = logging.getLogger('worker.worker_status')

def get_conn():
    return medareda_lib.get_conn()

def execute_sql(sql):
    f_logger.info(sql)
    _execute_sql(sql)

def _execute_sql(sql):
    for x in range(3):
        try:
            conn = get_conn()
            cur = conn.cursor()
        except Exception, e:
            f_logger.info(x)
            f_logger.exception(e)
            time.sleep(10)
            continue

        break

    f_logger.info(sql)
    cur.execute(sql)
    f_logger.info('DONE!!')

    try:
        result = cur.fetchall()
    except Exception, e:
        f_logger.exception(e)
        result = None

    conn.commit()
    cur.close()
    conn.close()
    return result

def getWorkerStatuses():
    sql = "SELECT count(*), status from  WorkerStatus GROUP BY status "
    result = execute_sql(sql)

    worker_statuses = {}
    for state in result:
        worker_statuses[state[1]] = state[0]
    return worker_statuses

def countWorkers(name):
    workers = getWorkerStatuses()
    #print workers
    rtn_count = 0
    for state,count in workers.items():
        #print state, count
        rtn_count += count
    return rtn_count

def addWorker(name):
    print 'Adding woker status'

    now = datetime.datetime.now()
    server_ip = 'ToDo'
    server_id = 0 # pull from name
    sql = "INSERT INTO WorkerStatus ( server_name, server_ip, serverId,status, since, rate) \
                     VALUES ('%s','%s','%s','%s','%s',%s)" %(name, server_ip, server_id,'build', now, 1 )

    execute_sql(sql)


def removeWorker(name):
    print 'Removing worker staus'
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.datetime.now()

    sql = "DELETE from WorkerStatus  WHERE server_name = '%s' " %(name)
    execute_sql(sql)



def updateWorkerStatus(name,status):
    f_logger.info('XXXX worker_status.updateWorkerStatus')
    print 'Update worker status to ', status

    now = datetime.datetime.now()
    #server_ip = 'ToDo'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = '%s' WHERE server_name = '%s' " %(status, name)
    f_logger.info(sql)
    execute_sql(sql)

    sql = "UPDATE WorkerStatus SET since = '%s' WHERE server_name = '%s' " %(now, name)
    execute_sql(sql)

def setWorkerStandby(name):
    now = datetime.datetime.now()
    #server_ip = 'ToDo'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = 'standby' WHERE server_name = '%s' " %( name)
    execute_sql(sql)
    sql = "UPDATE WorkerStatus SET since = '%s' WHERE server_name = '%s' " %(now, name)
    execute_sql(sql)


def setWorkerIP():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    sql = "UPDATE WorkerStatus SET server_ip = '%s' WHERE server_name = '%s' " %(ip, hostname)
    execute_sql(sql)


def getStatus(name):
    conn = get_conn()
    cur = conn.cursor()
    sql = "SELECT status from  WorkerStatus WHERE server_name = '%s' " %(name)
    cur.execute(sql)
    result = cur.fetchall()[0][0]
    conn.commit()
    cur.close()
    conn.close()
    return result
