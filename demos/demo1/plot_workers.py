# plot_workers.py

'''
plot the amount of processing each worker has done
and the duration of each bit of processing
'''



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker

import datetime

import medareda_lib

def get_conn():
    return medareda_lib.get_conn()


def plot():
    # show plot

    # show plot\n",
    fig1 = plt.figure(figsize=(5,11) )
    fig1.suptitle('MedaReda worker monitoring2')

    print 'Drawing plot'

    def animate1(i):
        connpg = get_conn()

        curpg = connpg.cursor()
        curpg.execute("select worker, count(*) from pPrice group by worker")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        display = {}
        for worker_name, count in results:
            #print worker_name, count
            display[worker_name] = count

        # dict = {'Asdfsdfsdfsd': 40, 'Bsdfadsf': 70, 'Casdfasdf': 30, 'Dadsfadsf': 85}
        # dict = results
        workers = display.keys()

        ax1 = fig1.add_subplot(3,1,1)
        ax1.clear()

        for i, key in enumerate(display):
            #print i,key
            ax1.bar(i, display[key], align = 'center')

        pos_list_ss = range(len(workers))
        ax1.xaxis.set_major_locator(ticker.FixedLocator(pos_list_ss))
        ax1.xaxis.set_major_formatter(ticker.FixedFormatter((workers)))
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=10, fontsize=10)

        # ---------------------------------------------------------------

        connpg = get_conn()

        curpg = connpg.cursor()
        curpg.execute("select pPriceID, idate, pstartdate, penddate from pPrice")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        x = []
        y1 = []
        y2 = []
        for p_price_id, i_date, p_start_date, p_end_date in results:
            #print p_price_id, i_date, p_start_date, p_end_date
            ya = p_start_date - i_date
            yb = p_end_date - p_start_date
            ya = ya.total_seconds() #+ 60*60 # due to time zone, 1 hour out
            yb = yb.total_seconds()
            x.append(p_price_id)
            y2.append(ya)
            y1.append(yb)

        #import numpy as np
    #
     #   fnx = lambda : np.random.randint(5, 50, 10)
      #  y = np.row_stack((fnx(), fnx(), fnx()))
       # x = np.arange(10)


        #y1, y2, y3 = fnx(), fnx(), fnx()


        ax2 = fig1.add_subplot(3,1,2)
        ax2.clear()
        #fig, ax2 = plt.subplots()
        #ax2.stackplot(x, y)
        #plt.show()

        #fig, ax = plt.subplots()
        ax2.stackplot(x, y2) #, y3)

        # ------------------------------------


        connpg = get_conn()

        curpg = connpg.cursor()
        curpg.execute("select pPriceID, idate, pstartdate, penddate from pPrice")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        x = []
        y1 = []
        y2 = []
        for p_price_id, i_date, p_start_date, p_end_date in results:
            #print p_price_id, i_date, p_start_date, p_end_date
            ya = p_start_date - i_date
            yb = p_end_date - p_start_date
            ya = ya.total_seconds() #+ 60*60 # due to time zone, 1 hour out
            yb = yb.total_seconds()
            x.append(p_price_id)
            y2.append(ya)
            y1.append(yb)

        #import numpy as np
    #
     #   fnx = lambda : np.random.randint(5, 50, 10)
      #  y = np.row_stack((fnx(), fnx(), fnx()))
       # x = np.arange(10)


        #y1, y2, y3 = fnx(), fnx(), fnx()


        ax3 = fig1.add_subplot(3,1,3)
        ax3.clear()
        ax3.stackplot(x, y1) #, y3)







    ani1 = animation.FuncAnimation(fig1,animate1, interval=2000)

    plt.show()

if __name__ == '__main__':
    plot()
