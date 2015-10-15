# plot10ccy.py

'''
Plot the ccy rates, and the product
'''


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime


import medareda_lib

def get_conn():
    return medareda_lib.get_conn()


# select count from vPrice
connpg = get_conn()
curpg = connpg.cursor()
curpg.execute("SELECT count(*) FROM vPrice;")
#print 'PG', curpg.fetchall()

connpg.commit()
curpg.close()
connpg.close()

def plot():
    fig1 = plt.figure()
    fig1.suptitle('CCY Prices')
    fig1.autofmt_xdate()

    ax1 = fig1.add_subplot(1,1,1)

    def animate1(i):
        connpg = get_conn()

        curpg = connpg.cursor()
        curpg.execute("SELECT date, price FROM vPrice where symbol = 'GBPUSD';")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        data = []
        x = []
        y = []

        for row in results:
            x.append(row[0])
            y.append(row[1])


        connpg = get_conn()
        curpg = connpg.cursor()
        curpg.execute("SELECT date, price FROM vPrice where symbol = 'USDEUR';")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        data2 = []
        x2 = []
        y2 = []

        for row in results:
            x2.append(row[0])
            #print row[1]
            y2.append(row[1])


        connpg = get_conn()
        curpg = connpg.cursor()
        curpg.execute("SELECT date, price FROM vPrice where symbol = 'EURGBP';")
        results =  curpg.fetchall()

        connpg.commit()
        curpg.close()
        connpg.close()

        data3 = []
        x3 = []
        y3 = []

        for row in results:
            x3.append(row[0])
            y3.append(row[1])


        connpg = get_conn()
        curpg = connpg.cursor()
        curpg.execute("SELECT date, combinedrate FROM vPrice ;")
        results =  curpg.fetchall()


        connpg.commit()
        curpg.close()
        connpg.close()

        data4 = []
        x4 = []
        y4 = []

        for row in results:
            x4.append(row[0])
            y4.append(row[1])

        ax1.clear()
        ax1.plot(x,y, '*-', label = 'GBPUSD')
        ax1.plot(x2,y2, '*-', label = 'USDEUR')
        ax1.plot(x3,y3,'*-', label = 'EURGBP')
        ax1.plot(x4,y4,'*-', label = 'Combined Rate')

        ax1.legend(loc='upper left')

        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation='vertical', fontsize=10)


    ani1 = animation.FuncAnimation(fig1,animate1, interval=2000)
    plt.show()

if __name__ == '__main__':
    plot()
