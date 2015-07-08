# %load medareda_lib
# %load medareda_lib.py
# medareda_lib

import urlparse
import psycopg2

def get_conn():
    DATABASE_URL= r"postgres://zpptclkw:_mnlCBXoH7PlxS6vGLC0lYfn3gEw5rpY@qdjjtnkv.db.elephantsql.com:5432/zpptclkw"
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(DATABASE_URL)

    connpg = psycopg2.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port)
    return connpg

def test():
    c = get_conn()
    print c
    c.close()
