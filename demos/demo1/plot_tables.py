# plot_tables.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import numpy as np

import medareda_lib

def get_conn():
    return medareda_lib.get_conn()

def count_iPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT count(*),status FROM iPrice group by status;")
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    res = {}
    for row in results:
        res[row[1]] = int(row[0])

        #rtn.append(  (row[1] , int(row[0]) ) )

    rtn = []
    rtn.append( ('wait',res.get('wait',0)))
    #rtn.append( ('process',res.get('process',0)))
    rtn.append( ('done',res.get('done',0)))
    #rtn.append( ('c',3))
    return rtn

def count_pPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM pPrice;")
    results =  cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    rtn = ( 'pPrice', int(results[0][0]))
    return rtn


def count_dPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM dPrice;")
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    rtn = ( 'dPrice', int(results[0][0]))
    return rtn


def count_vViewpoint():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT row FROM vViewpoint where dtable = 'dPrice';")
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    rtn = ( 'vViewpoint', int(results[0][0]))
    return rtn


def count_vPrice():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM vPrice;")
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    rtn = ( 'vPrice', int(results[0][0]))
    return rtn


def get_table_counts():
    counts = []

    for v in count_iPrice():
        counts.append ( v )

    counts.append( count_dPrice() )
    counts.append( count_pPrice() )
    counts.append( count_vViewpoint() )
    counts.append( count_vPrice() )
    return counts



def plot():
    fig1 = plt.figure()
    fig1.suptitle('Table counts')
    #fig1.autofmt_xdate()

    #ax1 = fig1.add_subplot(1,1,1)

    def animate1(i):

        data = [ ("data1", 34), ("data2", 22),
            ("data3", 11), ( "data4", 28),
            ("data5", 57), ( "data6", 39),
            ("data7", 23), ( "data8", 98)]
        data = get_table_counts()
        N = len( data )
        x = np.arange(1, N+1)
        y = [ num for (s, num) in data ]
        labels = [ s for (s, num) in data ]
        width = 1


        #plt.clear()
        fig1.clear()
        bar1 = plt.bar( x, y, width, color="y" )
        plt.ylabel( 'Count' )
        plt.xticks(x + width/2.0, labels )

    ani1 = animation.FuncAnimation(fig1,animate1, interval=2000)
    plt.show()

if __name__ == '__main__':
    plot()
