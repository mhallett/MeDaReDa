# %load medareda_lib
# %load medareda_lib.py
# medareda_lib

import ConfigParser
import urlparse
import psycopg2

def get_ini_data(section, names):
    parser = ConfigParser.SafeConfigParser()
    parser.read('./ini/medareda.ini')
    #parser.read('../ini/medareda.ini') # tmp to get local dir code running
    rtn = []
    for name in names:
        rtn.append( parser.get(section, name)  )
    #print rtn
    return rtn

def get_conn():
    (host, dbname, user, password) = get_ini_data ('worker',('host','dbname','user','password'))
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" %(host, dbname, user, password)
    conn = psycopg2.connect(conn_string)
    return conn

def get_pyrax_details():
    (default_region, user, password) = get_ini_data ('pyrax',('default_region','user','password'))
    return (default_region, user, password)



def test():
    c = get_conn()
    print c
    c.close()

    print 'pyrax ini'
    default_region, user, password = get_pyrax_details()
    print 'default_region: ', default_region
    print 'user: ', user

if __name__ == '__main__':
    # run from the directory above !!
    test()
