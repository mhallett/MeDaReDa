# process
# process input data


import time
import datetime
import socket
import logging
import logging.config

import medareda_lib

import dagCcy

logging.config.fileConfig('./ini/logging.conf')
#logging.basicConfig(filename='./log/process.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
#logger = logging.getLogger('__main__')

def get_conn():
    return medareda_lib.get_conn()


def getCombinedRate():
    logger.info('getCombinedRate')
    conn = get_conn()
    cur = conn.cursor()
    sql = "select distinct price, symbol from vPrice where date in (select max(date) from vPrice group by symbol)"
    cur.execute(sql)

    rows = cur.fetchall()
    conn.close()

    if len(rows) != 3:
        logger.info('len != 3: %s' %rows)
        return 0.0 #None
    #print "\nRows: \n"

    for row in rows:
        #print row
        rate = row[0]
        if row[1] == 'GBPUSD':
            dagCcy.MyDAG().set_a(rate)
            logger.debug('GBPUSD %s' %rate)
        if row[1] == 'USDEUR':
            dagCcy.MyDAG().set_b(rate)
            logger.debug('USDEUR %s' %rate)
        if row[1] == 'EURGBP':
            dagCcy.MyDAG().set_c(rate)
            logger.debug('EURGBP %s' %rate)

    product = dagCcy.MyDAG().get_d() #*= row[0]
    logger.debug('product %s' %product)
    #dagCcy.MyDAG().pp()
        #print "   ", row[1]

    #if (product < 0.9) or (1.1 < product):
    #    print product, rows

    return product


def processPrices(n=1):
    for i in range(n):
        processSinglePrice()

def processSinglePrice():

    #print 'process.processSinglePrice()'
    # get the next input row to process
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT min(iPriceId) FROM iPrice WHERE status = 'wait' ")
    row = c.fetchone()[0]

    #print row

    if row == None:
        #print 'No rows input table to process'
        return


    c.execute("UPDATE iPrice SET status = 'processing' WHERE iPriceID = %s" %row) #)) #, 'dPrice'))
    conn.commit()

    # select data to process
    c.execute("SELECT * FROM iPrice WHERE iPriceID = %s " %row )
    price_data = c.fetchone()
    #print price_data
    iPriceId = price_data[0]
    iDate = price_data[1]
    status = price_data[2]
    date = price_data[3]
    symbol = price_data[4]
    bid = price_data[5]
    rate = price_data[6]
    ask = price_data[7]

    #print ask

    # !! PROCESS DATA !!
    dconn = get_conn() #sqlite3.connect('data.db')
    dc = dconn.cursor()

    try:
        start = datetime.datetime.now()
        roll_ave = getCombinedRate() # not really but will do for first example

        #print 'roll_ave', roll_a

        error = 'good'
        time.sleep(2.0)
        end = datetime.datetime.now()


        # Insert data into data, and p table
        #print 'inserting into dTables'
        dPrice = ( iPriceId, iDate, start, end, date, symbol, bid, roll_ave, ask )

        dc.execute("INSERT INTO dPrice ( iDate, pStartDate, pEndDate, date,symbol,bid,roll_ave,ask) \
                           VALUES ('%s','%s','%s','%s','%s',%s,%s,%s)" %(iDate, start, end, date,symbol,bid,roll_ave,ask) )

        pPrice =   (iPriceId, iDate, start, end, error, date, symbol, bid, rate, ask )

        worker = socket.gethostname()


        sql = "INSERT INTO pPrice ( iDate, pStartDate, pEndDate, worker, error, date, symbol, bid, rate, ask)  \
                           VALUES ('%s','%s','%s','%s','%s','%s','%s',%s,%s,%s)" %(iDate, start, end, worker, error, date, symbol, bid, rate, ask)
        dc.execute(sql)

    except Exception, e:
        print 'ERROR !!!', str(e)
        #print 'sql:', sql
        print 'TODO write to pPrice ERROR msg'

    dconn.commit()
    dconn.close()

    # set in table to done
    conn = get_conn() #sqlite3.connect('in.db')
    c = conn.cursor()
    c.execute("UPDATE iPrice SET status = 'done' WHERE iPriceID = %s" %row) #)) #, 'dPrice'))
    conn.commit()
    conn.close()
    #print 'Done'

if __name__ == '__main__':
     print 'combined rate!', getCombinedRate()
     #print 'process single price!', processSinglePrice()
