# worker2.py


import datetime
import pyrax
import medareda_worker_lib
import os

class Worker2(object):
    
    def __init__(self,in_table):
        self.conn = medareda_worker_lib.get_conn()
        self.in_table = in_table
        
        self.server_id = self._getServerId()
        self.setStatusIdle()
        
    def _getServerId(self):
        hostname = os.uname()[1]
        server_id = hostname.split('-')[1]
        print server_id
        #return 4
        return int(server_id)


    def setStatusIdle(self):
        self._setStatus('idle')  
    
    def setStatusWorking(self):
        self._setStatus('working')
        
    def _setStatus(self, status):
        cur = self.conn.cursor()
        now = datetime.datetime.now()
    
        sql = "UPDATE Worker SET status = '%s', since = '%s' WHERE serverId = %s" %(status,now,self.server_id)
        cur.execute(sql)
        #print sql
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        
    def doWork(self):
        print 'process in data'
        # ( if status == deleting, return )
        # get amount of work to to
        # while work todo
        #   set worker status to work
        #   get work
        #   process work
        # set status to idle


def testWorker2():
    in_table = 'iPrice'
    w = Worker2(in_table)
    print w.server_id
    w.doWork()
    
testWorker2()