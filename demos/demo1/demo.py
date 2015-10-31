# demo.py

import time
import datetime
from yahoo_finance import Currency

import medareda_lib
import worker.office as office
import schema
import worker.office as office

def get_conn():
    return medareda_lib.get_conn()


def execute_sql(sql):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def clear_tables():
    schema.refresh_tables()
    return
    execute_sql('delete from workerstatus')
    execute_sql('delete from iprice')
    execute_sql('delete from dprice')
    execute_sql('delete from pprice')
    execute_sql('delete from vprice')
    execute_sql('delete from vprice')
    execute_sql("update vviewpoint set row = 0 where dtable = 'dPrice'")

# -------------------------------------------

def get_price(ticker):
    #print '-----------'
    #Currency('GBPUSD').refresh()
    bid = Currency(ticker).get_bid()
    rate = Currency(ticker).get_rate()
    ask = Currency(ticker).get_ask()

    trade_datetime  = Currency(ticker).get_trade_datetime ()

    print ticker, bid

    conn = get_conn()
    c  = conn.cursor()
    now = datetime.datetime.now()

    sql = "INSERT INTO iPrice (iDate,status,date,symbol,bid,rate,ask) VALUES ('%s','%s','%s','%s',%s,%s,%s) " %( now ,'wait',trade_datetime,ticker,bid,rate,ask)
    #print sql
    c.execute(sql)
    conn.commit()
    conn.close()
    return bid

def get_prices(i=1):
    for x in range(i):
        for ticker in ('GBPUSD','EURGBP','USDEUR'):
            get_price(ticker)

def create_office():
    work = 'iprice'
    start_workers = 4
    o_mgr = office.OfficeManager(work,start_workers)


def set_workers(status):
    print 'set workers', status
    sql = "update workerstatus set status = '%s'" %(status)
    execute_sql(sql)

if __name__ == '__main__':
    print 'test demo'
    schema.refresh_tables()
