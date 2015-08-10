# server.py

import os
import sys
import collections
import datetime
import pyrax
import ConfigParser
#import medareda_worker_lib

def get_ini_values():
    ini_values = {}

    filename = r'../ini/medareda.ini'
    if not os.path.exists(filename):
        print 'No medareda ini file'
        sys.exit(3)

    parser = ConfigParser.SafeConfigParser()
    parser.read(filename)

    # if using pyrax
    ini_values['default_region'] = parser.get('pyrax', 'default_region')
    ini_values['user'] = parser.get('pyrax', 'user')
    ini_values['password'] = parser.get('pyrax', 'password')

    return ini_values


def get_cs():
    # read from config file
    ini_values = get_ini_values()
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_default_region(ini_values['default_region'])
    pyrax.set_credentials(ini_values['user'], ini_values['password'])

    cs = pyrax.cloudservers
    return cs


def server_states(base_name):
    cs = get_cs() #self.get_cs()
    servers = pyrax.cloudservers.list()

    counter = collections.Counter()
    for s in servers:
        if s.name.startswith(base_name):
            counter[s.status] += 1
    return counter


def countServers(base_name):
    states = server_states(base_name)
    total = 0
    for name, value in states.items():
        total += value
    return total


def _create_server(cs,name,image_id,flavor_id):
        print 'create server ...'
        server = cs.servers.create(name,image_id,flavor_id)

def createServer(base_name,image_name):

        name = '%s-%s' %(base_name,countServers(base_name)+1)
        print 'create new server, called', name

        cs = get_cs()

        msg = 'from image %s' %image_name
        print msg
        image = None
        for i in cs.list_images():
            if i.name == image_name:
                image = i
                break

        flavor = cs.list_flavors()[0]

        server = _create_server(cs,name, image.id, flavor.id)
        return name

    #def getStatus(self):
    #    return self.status

        #cur = self.conn.cursor()
        #sql = "SELECT status FROM Worker WHERE serverId = %s" %(self.server_id)
        #cur.execute(sql)
        #status = cur.fetchone()[0]
        #self.conn.close()
        #print status
        #return status

def _delete(server):
    server.delete()

def delete(base_name):
        #if status == 'idle':
        # set worker row to deleting
        count = countServers(base_name)
        if count == 0:
            print 'No server found to delete'
            return

        remove_name = '%s-%s' %(base_name,count)
        print 'Remove ', remove_name
        cs = get_cs()
        sacrifice = cs.servers.find(name=remove_name)
        status = sacrifice.status
        if status == "BUILD":
            print 'Wont delete building server ', remove_name
            return None
        else:
            #mark to do no more work
            # wait till no more jobs with this server
            #w = worker_status.WorkerStatus(remove_name)
            #w.removeWorker()
            _delete(sacrifice)
            return remove_name
            #sacrifice.delete()



        #self.server.delete()



        #remove row , do in lev
        '''
        cur = self.conn.cursor()
        sql = "DELETE FROM Worker WHERE serverId = %s" %(self.server_id)
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()
        '''
