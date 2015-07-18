# %load medareda_lib
# %load medareda_lib.py
# medareda_lib

import urlparse
import psycopg2

def get_conn_old():
    DATABASE_URL= r"postgres://zpptclkw:_mnlCBXoH7PlxS6vGLC0lYfn3gEw5rpY@qdjjtnkv.db.elephantsql.com:5432/zpptclkw"
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(DATABASE_URL)

    connpg = psycopg2.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port)
    return connpg


def get_ini_data(section, names):  
    parser = ConfigParser.SafeConfigParser()  
    parser.read('../ini/medareda.ini')
    rtn = []
    for name in names:
        rtn.append( parser.get(section, name)  )
    return rtn

def get_conn():
    (host, dbname, user, password) = get_ini_data ('worker',('host','dbname','user','password'))
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" %(host, dbname, user, password)
    conn = psycopg2.connect(conn_string)
    return conn


def test():
    c = get_conn()
    print c
    c.close()
