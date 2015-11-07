# worker_status.py

import datetime
import medareda_lib

def get_conn():
    return medareda_lib.get_conn()

def _execute_sql(sql):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    try:
        result = cur.fetchall()
    except:
        result = None
    conn.commit()
    cur.close()
    conn.close()
    return result
    # use finally

def getWorkerStatuses():
    sql = "SELECT count(*), status from  WorkerStatus GROUP BY status "
    result = _execute_sql(sql)

    worker_statuses = {}
    for state in result:
        worker_statuses[state[1]] = state[0]
    return worker_statuses

def getServersNameStatus(basename):
    sql = "SELECT server_name, status from  WorkerStatus where server_name like '%s%%'" %(basename)
    result = _execute_sql(sql)
    return result


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

    _execute_sql(sql)


def removeWorker(name):
    print 'Removing worker staus'
    ##conn = get_conn()
    ##cur = conn.cursor()
    now = datetime.datetime.now()

    sql = "DELETE from WorkerStatus  WHERE server_name = '%s' " %(name)
    _execute_sql(sql)



def updateWorkerStatus(name,status):
    print 'Update worker status to ', status

    now = datetime.datetime.now()
    #server_ip = 'ToDo'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = '%s',since = '%s' WHERE server_name = '%s' " %(status, now, name) #NEW
    _execute_sql(sql)


def setWorkerWorking(name):
    print 'Update worker status to work'

    now = datetime.datetime.now()
    #server_ip = 'TODO'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = 'work' WHERE server_name = '%s' " %( name)
    _execute_sql(sql)

def setWorkerStandby(name): # for start up
    #now = datetime.datetime.now()
    updateWorkerStatus(name,'standby')
    server_ip = 'IP'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET server_ip = '%s' WHERE server_name = '%s' " %(server_ip, name)
    _execute_sql(sql)

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


def test_WorkerStatuses():
    sql  = "SELECT * from  WorkerStatus"
    result = _execute_sql(sql)
    print 'result: ', result

def test_getWorkerStatuses():
    print 'getWorkerStatuses'
    statuses = getWorkerStatuses()
    print 'statuses: ', statuses

def test():
    test_WorkerStatuses()
    #test_getWorkerStatuses()

if __name__ == '__main__':
    print 'test'
    test()
