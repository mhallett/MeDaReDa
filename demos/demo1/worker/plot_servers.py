# plot_servers.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import datetime
import numpy as np
import ConfigParser

import medareda_lib
import worker_status

#import urllib3
#urllib3.disable_warnings()
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


import medareda_lib

def get_conn():
    return medareda_lib.get_conn()



import pyrax
import collections
import medareda_lib

def get_server_states():
    base_name = 'medaredaworker-'

    pyrax.set_setting("identity_type", "rackspace")
    default_region, user, password = medareda_lib.get_pyrax_details()
    pyrax.set_default_region(default_region)
    pyrax.set_credentials(user, password)

    #cs = pyrax.cloudservers
    servers = pyrax.cloudservers.list()

    states = []
    counter = collections.Counter()
    for s in servers:
        if s.name.startswith(base_name):
            counter[s.status] += 1
            #print s.name, 'found'
            #states.append(s.status)
        #else:
        #    print 'not counted', s.name

    #counter = collections.Counter()
    #for word in states:
    #    counter[word] += 1


    return counter

def get_iPrice_status():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT count(*),status FROM iPrice group by status;")
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    rtn = {}
    for r in results:
        rtn[r[1]] = r[0]
    return rtn


def plot():
    # show plot\n",
    fig1 = plt.figure(figsize=(4,11) )
    fig1.suptitle('MedaReda worker monitoring')

    #connpg = get_conn()\n",
    #curpg = connpg.cursor()\n",
    print 'Drawing plot'
    def animate1(i):

        # 1 -------------------
        #server_statuses = ('Build','Standby','Active','Cooldown')
        server_statuses = ('Build','Active')


        states = get_server_states()
        #print states

        pos_list_ss = range(2) #len(states))\n",

        standby = 0.001
        cooldown = 0.001

        building = states.get('BUILD',0.001)
        working = states.get('ACTIVE',0.001) # - standby cooldown
        #idle = states.get('IDLE',0.001)

        if building == 0.001:
            if working == 0.001:
                if standby == 0.001:
                    if cooldown == 0.001:
                        building =  working = standby = cooldown = 0


        ax1 = fig1.add_subplot(3,1,1)
        ax1.clear()
        ax1.xaxis.set_major_locator(ticker.FixedLocator(pos_list_ss))
        ax1.xaxis.set_major_formatter(ticker.FixedFormatter((server_statuses)))
        plt_r = plt.bar(pos_list_ss, (building,0),color = 'r', align = 'center')
        #plt_y = plt.bar(pos_list_ss, (0,standby,0,0) ,color = 'y', align = 'center')
        plt_g = plt.bar(pos_list_ss, (0,working) ,color = 'g', align = 'center')
        #plt_b = plt.bar(pos_list_ss, (0,0,0,cooldown) ,color = 'b', align = 'center')

        ax1.set_xlabel('State of Servers')


        # 2 -----------

        statuses = ('Build','Standby','Work','Cooldown')
        states = get_server_states()
        #print states

        pos_list = range(4) #len(states))\n",

        standby = 0.001
        cooldown = 0.001

        worker_statuses = worker_status.getWorkerStatuses()

        #print worker_statuses

        building = worker_statuses.get('build',0.001) #states.get('BUILD',0.001)
        standby = worker_statuses.get('standby',0.001)
        working = worker_statuses.get('work',0.001) #3 #states.get('ACTIVE',0.001) # - standby cooldown
        cooldown = worker_statuses.get('cooldown',0.001)  #1 # = states.get('IDLE',0.001)

        if building == 0.001:
            if working == 0.001:
                if standby == 0.001:
                    if cooldown == 0.001:
                        building =  working = standby = cooldown = 0

        ax2 = fig1.add_subplot(3,1,2)
        ax2.clear()
        ax2.xaxis.set_major_locator(ticker.FixedLocator(pos_list))
        ax2.xaxis.set_major_formatter(ticker.FixedFormatter((statuses)))
        plt_r = plt.bar(pos_list, (building,0,0,0),color = 'r', align = 'center')
        plt_y = plt.bar(pos_list, (0,standby,0,0) ,color = 'y', align = 'center')
        plt_g = plt.bar(pos_list, (0,0,working,0) ,color = 'g', align = 'center')
        plt_b = plt.bar(pos_list, (0,0,0,cooldown) ,color = 'b', align = 'center')
        ax2.set_xlabel('State of Workers')

        # 3 -----------
        work_states = ('Wait','Process','Error')
        iPrice_states = get_iPrice_status()
        pos_wk_list = range(3)
        wk_wait = iPrice_states.get('wait',0.001)
        wk_processing = iPrice_states.get('processing',0.001)
        wk_error = iPrice_states.get('error',0.001)

        if wk_wait == 0.001:
            if wk_processing == 0.001:
                if wk_error == 0.001:
                    wk_wait =  wk_processing = wk_error = 0

        #ax = plt.axes()

        #ax1.set_ylabel('Count')


        ax3 = fig1.add_subplot(3,1,3)
        ax3.clear()
        ax3.xaxis.set_major_locator(ticker.FixedLocator(pos_wk_list))
        ax3.xaxis.set_major_formatter(ticker.FixedFormatter((work_states)))
        plt_r3 = plt.bar(pos_wk_list, (wk_wait,0,0),color = 'b', align = 'center')
        plt_g3 = plt.bar(pos_wk_list, (0,wk_processing,0) ,color = 'g', align = 'center')
        plt_y3 = plt.bar(pos_wk_list, (0,0,wk_error) ,color = 'r', align = 'center')
        ax3.set_xlabel('State of inPrices')
        #ax2.set_ylabel('Count')

    ani1 = animation.FuncAnimation(fig1,animate1, interval=2000)
    plt.show()

if __name__ == '__main__':
    plot()
