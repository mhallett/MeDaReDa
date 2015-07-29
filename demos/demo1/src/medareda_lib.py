# %load medareda_lib
# %load medareda_lib.py
# medareda_lib

import urlparse
import psycopg2
import ConfigParser

def get_ini_data(section, names):  
    parser = ConfigParser.SafeConfigParser()  
    #parser.read('/root/medareda/demos/demo1/ini/medareda.ini')
    parser.read('../ini/medareda.ini')
    rtn = []
    for name in names:
        rtn.append( parser.get(section, name)  )
    return rtn

def get_conn():
    (host, dbname, user, password) = get_ini_data ('worker',('host','dbname','user','password'))
    print '2 host',host
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" %(host, dbname, user, password)
    conn = psycopg2.connect(conn_string)
    return conn


def test():
    c = get_conn()
    print c
    c.close()
