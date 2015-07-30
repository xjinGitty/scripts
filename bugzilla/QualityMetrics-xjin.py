import sys
from operator import itemgetter

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient

client = MongoClient('mongodb://147.2.212.204:27017/')
prods = client.bz.prods

prod_all = [  'SUSE Linux Enterprise Desktop 12',
              'SUSE Linux Enterprise Desktop 11 SP3',
              'SUSE Linux Enterprise Desktop 11 SP4 (SLED 11 SP4)']

teamMem = ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com',
           'ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com',
           'yosun@suse.com','nwang@suse.com','bchou@suse.com']

validreso = ['FIXED','UPSTEAM','NORESPONSE','---','MOVED']
invalidreso = ['INVALID','WONTFIX','DUPLICATE','FEATURE','WORKSFORME']
severity = ['Enhancement',]

query_limit = {'product':1, 'component':1, 'creator':1, 'resolution':1,
               'severity':1, '_id':0}
result = prods.find({'product':{'$in':prod_all}}, query_limit)
data = [i for i in result]
print(sys.getsizeof(data))

comps = list(set([i['component'] for i in data]))

def get_count(products=[], comps=[], resolutions=[], severitys=[], creators=[]):
    count = 0
    for d in data:
        if products:
            if d['product'] not in products:
                continue
        if comps:
            if d['component'] not in comps:
                continue
        if resolutions:
            if d['resolution'] not in resolutions:
                continue
        if severitys:
            if d['severity'] in severitys:
                continue
        if creators:
            if d['creator'] not in creators:
                continue
        count += 1
    return count

###############  component comparision statistic  ################
# default result is compValid/compAll; could select compValid/allValid
def plt_comp(arg):
    N = len(comps)
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        allvalids = get_count([prod,], , validreso, , )
        for comp in comps:
            allcomps = get_count([prod,], [comp,])
            if arg:
                allnums = allvalids
                picname = "totalcompvalidincompall.png"
            else:
                allnums = allcomps
                picname = "totalcompvalidinallvalid.png"
            if allnums:
                validcomps = get_count([prod,], [comp,], validreso)
                axis_y.append(validcomps/allnums)
            else:
                axis_y.append(0)
        
        rects = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        count += 1
    plt.axis([0, 2*N+2, 0, 1.2])
    plt.savefig(picname)

##############  EBR statistic (based on team data)  ################
# default is team's result; could select total's result
def plt_allandvalid(arg):
    N = 3 
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    if arg:
        picname = "totalallandvalidnumber.png"
        tmpList = None
    else:
        picname = "teamallandvalidnumber.png"
        tmpList = teamMem
    for prod in prod_all:
        ind = [i*4+count*1.0 for i in range(N)]
        axis_y[0] = get_count([prod,], , , ,tmpList)
        axis_y[1] = get_count([prod,], ,invalidreso, ,tmpList) + 
                    get_count([prod,], , ,['Enhancement',],teamMem) 
        axis_y[2] = axis_y[1]/axis_y[0]*100
        rects = ax.bar(ind, axis_y, 1.0, color=colors[count])        
        count += 1
    plt.axis([0, 2*N+2, 0, 1.2])
    plt.savefig(picname)

def plt_invalidtype():
    N = len(invalidreso) + 1
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    for prod in prod_all:
        axis_y = []
        ind = [i*4+count*1.0 for i in range(N)]
        teamall = get_count([prod,], , , ,teamMem)
        for invalidtype in invalidreso:
            invalids = get_count([prod,], ,[invalidtype,], , teamMem)
            axis_y.append(invalids/teamall)
        severitys =  get_count([prod,], , ,['Enhancement',], teamMem)
        axis_y.append(severitys/teamall)
        rects = ax.bar(ind, axis_y, 1.0, color=colors[count])        
        count += 1
    plt.axis([0, 2*N+2, 0, 1.2])
    plt.savefig('teamtyperatio.png')

# default is in all ratio; could select in all-invalid ratio
def plt_invalidcomp(arg):
    N = len(comps)
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        if arg:
            picname = "teamcompALLINVALIDratio.png"
            allnums = get_count([prod,], ,invalidreso, ,teamMem) + 
                            get_count([prod,], , ,['Enhancement',], teamMem) 
        else:
            picname = "teamcompinALLratio.png"
            allnums = get_count([prod,], , , ,teamMem)
        for comp in comps:
            invalidcomps = get_count([prod,], [comp,], invalidreso, ,teamMem) + 
                            get_count([prod,], [comp,], ,['Enhancement',] ,teamMem) 
            axis_y.append(validcomps/allnums)
        
        rects = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        count += 1
    plt.axis([0, 2*N+2, 0, 1.2])
    plt.savefig(picname)

plt_allandvalid(1)
plt_comp()
plt_comp(1)

plt_allandvalid()
plt_invalidtype()
plt_invalidcomp()
plt_invalidcomp(1)

def plt_label():
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
    
    #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
    
    # attach some text labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
