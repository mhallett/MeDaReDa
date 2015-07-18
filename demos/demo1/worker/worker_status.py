# worker_status.py

import datetime
import medareda_worker_lib

def get_conn():
    return medareda_worker_lib.get_conn()

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

def getWorkerStatuses():
    sql = "SELECT count(*), status from  WorkerStatus GROUP BY status " 
    result = _execute_sql(sql)
    
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

    _execute_sql(sql)
        

def removeWorker(name):
    print 'Removing worker staus'
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.datetime.now()

    sql = "DELETE from WorkerStatus  WHERE server_name = '%s' " %(name)
    _execute_sql(sql)

        

def updateWorkerStatus(name,status):
    print 'Update worker status to ', status

    now = datetime.datetime.now()
    #server_ip = 'ToDo'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = '%s' WHERE server_name = '%s' " %(status, name)
    _execute_sql(sql)
    
    
def setWorkerWorking(name):
    print 'Update worker status to work'

    now = datetime.datetime.now()
    #server_ip = 'ToDo'
    #server_id = self.wkr_id
    sql = "UPDATE WorkerStatus SET status = 'work' WHERE server_name = '%s' " %( name)
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
    