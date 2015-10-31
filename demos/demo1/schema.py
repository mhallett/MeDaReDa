# schema.py

import medareda_lib

def get_conn():
    return medareda_lib.get_conn()

def create_iPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS iPrice   ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS iPrice  ( \
                 iPriceId SERIAL PRIMARY KEY, \
                 iDate timestamp,
                 status text,
                 date timestamp, symbol text, bid real, rate real, ask real)''')
    conn.commit()
    cur.close()
    conn.close()


def create_vPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS vPrice   ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS vPrice
                    ( vPriceId serial PRIMARY KEY,
                      date timestamp,
                      symbol text,
                      price real,
                      combinedRate real)''')
    conn.commit()
    cur.close()
    conn.close()


def create_pPrice():
    conn = get_conn()
    c  = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS pPrice   ''')

    c.execute('''CREATE TABLE IF NOT EXISTS pPrice  (  \
                          pPriceId SERIAL PRIMARY KEY, \
                          iPriceID integer, \
                          iDate timestamp, \
                          pStartDate timestamp, \
                          pEndDate timestamp, \
                          worker text, \
                          error text, \
                          date timestamp, symbol text, bid real, rate real, ask real)             ''')
      # no audit or market or type
    conn.commit()
    conn.close()


def create_dPrice():
    conn = get_conn()
    c  = conn.cursor()
    c.execute("DROP TABLE IF EXISTS dPrice ")
    c.execute('''CREATE TABLE IF NOT EXISTS dPrice  (\
                   dPriceId SERIAL PRIMARY KEY, \
                   iPriceId integer, \
                   iDate timestamp, \
                   pStartDate timestamp, \
                   pEndDate timestamp, \
                   date timestamp, symbol text, bid real, roll_ave real, ask real)''')
       # no audit or market or type

    conn.commit()
    conn.close()


def register_price():
    print 'register_price'
    conn = get_conn()
    c = conn.cursor()
    viewpoint = [('dPrice', 0),]
    c.execute("INSERT INTO vViewpoint (dtable, row) VALUES ('dPrice',0)" )
    conn.commit()

    conn.close()


def create_vViewpoint():
    conn = get_conn()
    c  = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS vViewpoint   ''')
    c.execute('''CREATE TABLE IF NOT EXISTS vViewpoint ( vViewpointId SERIAL PRIMARY KEY, dtable text, row int)''')
       # id should be int

    conn.commit()
    conn.close()


def refresh_tables():
    print 'refresh_tables'
    create_iPrice()
    create_pPrice()
    create_dPrice()
    create_vPrice()
    create_vViewpoint()
    register_price()
    print 'Done'


if __name__ == '__main__':
    refesh_tables()
