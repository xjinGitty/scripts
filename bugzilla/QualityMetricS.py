#! /usr/bin/python3
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

dct_comps = {}
for i in data:
	comp = i['component']
	if comp in dct_comps:
		dct_comps[comp] += 1
	else:
		dct_comps[comp] = 1
lst_comps = list(dct_comps.items())
lst_comps = sorted(lst_comps, key=itemgetter(1), reverse=True)[:20]
top20_comps = [i[0] for i in lst_comps[:20]]
print(top20_comps)

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
            if d['severity'] == 'Enhancement' :
                continue
        if severitys:
            if d['severity'] in severitys:
                continue
        if creators:
            if d['creator'] not in creators:
                continue
        count += 1
    return count

############### label function ###############
def plt_label(ax,rects,title,xlabel,width, heightest):
    # add some text for labels, title and axes ticks
    ax.set_ylabel('bugNumber / ratio %')
    ax.set_title(title)
    np_xlabel=np.arange(0.5, 2*len(xlabel), 2)
    ax.set_xticks(np_xlabel)
    print(np_xlabel)
    #ax.xticks(np.arange(2*len(xlabel) +2))
    ax.set_xticklabels(xlabel, horizontalalignment='center',
		rotation=50, size='xx-small')
    
    #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
    ax.legend( rects, prod_all )
    
    # attach some text labels
    def autolabel(rects, heightest):
        for rect in rects:
            height = rect.get_height()
            value = height if height > 1 else 1000 * height
            ax.text(rect.get_x()+rect.get_width()/2., heightest, '%3.0f'% value,
                    ha='center', va='bottom')
    if heightest:
        for i in rects:
            autolabel(i, heightest)
            heightest = heightest * 0.95

###############  component comparision statistic  ################
# default result is compValid/compAll; could select compValid/allValid
def plt_comp(arg):
    N = len(top20_comps)
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    height = []
    rects = []
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        allvalids = get_count(products=[prod,],resolutions=validreso )
        for comp in top20_comps:
            allcomps = get_count(products=[prod,], comps=[comp,])
            if arg:
                allnums = allvalids
                picname = "totalcompvalidincompall"
            else:
                allnums = allcomps
                picname = "totalcompvalidinallvalid"
            if allnums:
                validcomps = get_count([prod,], [comp,], validreso, [], [])
                axis_y.append(validcomps/allnums)
            else:
                axis_y.append(0)
        
        rect = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        rects.append(rect)
        count += 1
        height.append(sorted(axis_y,reverse=True)[0])
    heightest = sorted(height, reverse=True)[0]
    height = heightest * 1.3
    plt.axis([0, 2*N, 0, height])
    plt_label(ax,rects,picname,top20_comps,0.5, 0)
    plt.gca().grid(True)
    plt.savefig(picname+".png")

##############  EBR statistic (based on team data)  ################
# default is team's result; could select total's result
def plt_allandvalid(arg):
    N = 3 
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    height = []
    rects = []
    if arg:
        picname = "totalallandvalidnumber"
        tmpList = None
    else:
        picname = "teamallandvalidnumber"
        tmpList = teamMem
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        axis_y.append(get_count([prod,],[] , [] , [] ,tmpList))
        axis_y.append(get_count([prod,], [] ,invalidreso, [] ,tmpList) + get_count([prod,], [] , [] ,['Enhancement',],teamMem) )
        axis_y.append(axis_y[1]/axis_y[0]*100)
        rect = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        rects.append(rect)
        count += 1
        height.append(sorted(axis_y,reverse=True)[0])
    heightest = sorted(height, reverse=True)[0]
    height = heightest * 1.4
    plt.axis([0, 2*N, 0, height])
    plt_label(ax,rects,picname,["all","valid","EBR"],0.5, heightest)   
    plt.savefig(picname+".png")

def plt_invalidtype():
    N = len(invalidreso) + 1
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    height = []
    rects = []
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        teamall = get_count([prod,], [] , [] , [] ,teamMem)
        for invalidtype in invalidreso:
            invalids = get_count([prod,], [] ,[invalidtype,], [] , teamMem)
            axis_y.append(invalids/teamall)
        severitys =  get_count([prod,], [] , [] ,['Enhancement',], teamMem)
        axis_y.append(severitys/teamall)
        rect = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        rects.append(rect)
        count += 1
        height.append(sorted(axis_y,reverse=True)[0])
    heightest = sorted(height, reverse=True)[0]
    height = heightest * 1.4
    plt.axis([0, 2*N, 0, height])
    tmpinvalidreso = invalidreso
    tmpinvalidreso.append("teamSeverity")
    plt_label(ax,rects,"teaminvalidtyperatio",tmpinvalidreso,0.5, heightest)   
    plt.savefig('teamtyperatio.png')

# default is in all ratio; could select in all-invalid ratio
def plt_invalidcomp(arg):
    N = len(top20_comps)
    count = 0
    colors = ['r', 'y', 'g']
    fig, ax = plt.subplots()
    height = []
    rects = []
    for prod in prod_all:
        axis_y = []
        ind = [i*2+count*0.5 for i in range(N)]
        if arg:
            picname = "teamcompALLINVALIDratio"
            allnums = get_count([prod,], [] ,invalidreso, [] ,teamMem) + get_count([prod,], [] , [] ,['Enhancement',], teamMem) 
        else:
            picname = "teamcompinALLratio"
            allnums = get_count([prod,], [] , [] , [] ,teamMem)
        for comp in top20_comps:
            invalidcomps = get_count([prod,], [comp,], invalidreso, [] ,teamMem) + get_count([prod,], [comp,], [] ,['Enhancement',] ,teamMem) 
            axis_y.append(invalidcomps/allnums)
        
        rect = ax.bar(ind, axis_y, 0.5, color=colors[count])        
        rects.append(rect)
        count += 1
        height.append(sorted(axis_y,reverse=True)[0])
    heightest = sorted(height, reverse=True)[0]
    height = heightest * 1.3
    plt.axis([0, 2*N+2, 0, height])

    plt_label(ax,rects,picname,top20_comps,0.5, 0)
    plt.gca().grid(True)
    plt.savefig(picname+".png")

plt_allandvalid(1)
plt_comp(0)
plt_comp(1) 
plt_allandvalid(0)
plt_invalidtype()
plt_invalidcomp(0)
plt_invalidcomp(1)

