# process
# process input data


import time
import datetime
import logging

import medareda_lib

f_logger = logging.getLogger(__name__)

def get_conn():
    f_logger.info('get_conn')
    return medareda_lib.get_conn()


def processSinglePrice():
    # get the next input row to process
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT min(iPriceId) FROM iPrice WHERE status = 'wait' ")
    row = c.fetchone()[0]
    
    if row == None:
        f_logger.info('No rows to input rows to process')
        return
        
    c.execute("UPDATE iPrice SET status = 'processing' WHERE iPriceID = %s" %row) #)) #, 'dPrice'))
    conn.commit()
    
    # select data to process
    c.execute("SELECT * FROM iPrice WHERE iPriceID = %s " %row )
    price_data = c.fetchone()
    f_logger.info(price_data)
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
        roll_ave = (rate + ask ) /2 # not really but will do for first example
        error = 'good'
        time.sleep(2.0/60.0)
        end = datetime.datetime.now()
    
        # Insert data into data, and p table
        #print 'inserting into dTables'
        dPrice = ( iPriceId, iDate, start, end, date, symbol, bid, roll_ave, ask )
        #dc.execute('INSERT INTO dPrice (iPriceId, iDate, pStartDate, pEndDate, date,symbol,bid,roll_ave,ask) \
        #                   VALUES (?,?,?,?,?,?,?,?,?)', dPrice)
    
        dc.execute("INSERT INTO dPrice ( iDate, pStartDate, pEndDate, date,symbol,bid,roll_ave,ask) \
                           VALUES ('%s','%s','%s','%s','%s',%s,%s,%s)" %(iDate, start, end, date,symbol,bid,roll_ave,ask) )
        
        pPrice =   (iPriceId, iDate, start, end, error, date, symbol, bid, rate, ask )
        #dc.execute('INSERT INTO pPrice (iPriceId, iDate, pStartDate, pEndDate, error, date, symbol, bid, rate, ask)  \
        #                   VALUES (?,?,?,?,?,?,?,?,?,?)', pPrice)
        
        dc.execute("INSERT INTO pPrice ( iDate, pStartDate, pEndDate, error, date, symbol, bid, rate, ask)  \
                           VALUES ('%s','%s','%s','%s','%s','%s',%s,%s,%s)" %(iDate, start, end, error, date, symbol, bid, rate, ask)  )
            
    except Exception, e:
        print 'ERROR !!!', str(e)
        f_logger.exception('Writting price to dPrice')
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
