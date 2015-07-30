#! /usr/bin/python3
import matplotlib
import operator
from operator import itemgetter
import sys
matplotlib.use("PS")
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from pprint import pprint
from pymongo import MongoClient
client = MongoClient('mongodb://147.2.212.204:27017/')
prods = client.bz.prods

# common data structure
prod_all = [  'SUSE Linux Enterprise Desktop 12',
              'SUSE Linux Enterprise Desktop 11 SP3',
              'SUSE Linux Enterprise Desktop 11 SP4 (SLED 11 SP4)']

teamMem = ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com','ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com','yosun@suse.com','nwang@suse.com','bchou@suse.com']

validreso = ['FIXED','UPSTEAM','NORESPONSE','---','MOVED']
invalidreso = ['INVALID','WONTFIX','DUPLICATE','FEATURE','WORKSFORME']

compA = prods.find({'product':{'$in':prod_all} })
compl = [i['component'] for i in compA]
comps = set(compl)
# EBR specific data structure
teamBugA = {}
teamBugV = {}
teamValidRatio = {}
teamInvalidNum = {}
teamInvalidComp = {}

# product level specific data structure
totalBugA = {}
totalBugV = {}
totalValidRatio = {}
totalValidComp = {}

# pre-define function
def compSelect(D):
    dictT = {}
    listT = []
    for prod in prod_all:
        for comp in comps:
            dictT[comp+'InAllRatiotrue'] = D[prod][comp+'InAllRatiotrue']
        listT.append( sorted(dictT,key=itemgetter(1)) )
    
    return [comp for comp in listT[0] if comp in listT[1] and comp in listT[2]][:20]

def RatioConvert(arg):
    return str(arg * 100)[:5]+ '%'

teamChartDict = {}
#======================EBR data==========================
### EBR related statistic: we just consider for bugs reported by QA APACI
def EBRStatis(prod):
    ## all bug number
    teamA = prods.find({'product': prod,'creator': {'$in':teamMem} }).count()
    #    teamAL = [teamAL.expand(i) for i in compA if i['product'] == prod and i['creator'] in teamMem]
    teamBugA[prod] = teamA 
    
    ## valid bug number
    teamV = prods.find({'product': prod,'creator': {'$in': teamMem},'resolution':{'$in': validreso},'severity':{'$ne':'Enhancement'} }).count()
    teamBugV[prod] = teamV 
    
    ## EBR ratio
    TVratio = RatioConvert(teamV/teamA)
    teamValidRatio[prod] = TVratio
    
    ## invalid bug number statistic
    # all invalid bug number
    teamI = teamA - teamV
    # INVALID # WONTFIX # DUPLICATE # WORKSFORME # bug num
    tmpDict = teamInvalidNum.setdefault(prod, {})
    for reso in invalidreso:
        tmp = prods.find({'product': prod,'creator': {'$in': teamMem},'resolution':reso}).count()
        tmpDict[reso] = tmp
    #== each invalid type/all ratio??==#== each invalid type/all invalid ratio??
        tmpTypeRatio = reso+'InAllRatio'
        tmpDict[tmpTypeRatio] = RatioConvert(tmp/teamA)
        temInvalidRatio = reso+'Ratio'
        tmpDict[temInvalidRatio] = RatioConvert(tmp/teamI)
        tmpTypeRatiotrue = reso+'InAllRatiotrue'
        tmpDict[tmpTypeRatiotrue] = tmp/teamA
        temInvalidRatiotrue = reso+'Ratiotrue'
        tmpDict[temInvalidRatiotrue] = tmp/teamI
    ## ENHANCEMENT
    temEnhance = prods.find({'product': prod,'creator': {'$in': teamMem},'severity':'Enhancement'}).count()
    tmpDict['EnhanceSeve'] = temEnhance
    tmpDict['EnhanceSeveAllRatio'] = RatioConvert(temEnhance/teamA)
    tmpDict['EnhanceSeveInvalidRatio'] = RatioConvert(temEnhance/teamI)
    tmpDict['EnhanceSeveAllRatiotrue'] = temEnhance/teamA
    tmpDict['EnhanceSeveInvalidRatiotrue'] = temEnhance/teamI
    
    ## each component invalid/ total invalid ratio
    temCompDict = teamInvalidComp.setdefault(prod,{})
    teamChartD = teamChartDict.setdefault(prod, {})
    for comp in comps:
        temComp = prods.find({'product': prod,'creator': {'$in': teamMem},'component':comp,'resolution': {'$in':invalidreso}, 'severity':'Enhancement' }).count()
        if temComp == 0:
            continue
        temCompDict[comp] = temComp
        temComINA = comp + 'InAlldRatio'
        temCompDict[temComINA] = RatioConvert(temComp/teamA)
        temComIN = comp + 'Ratio'
        temCompDict[temComIN] = RatioConvert(temComp/teamI)
        temComINAtrue = comp + 'InAlldRatiotrue'
        print(temComINAtrue)
        temCompDict[temComINAtrue] = temComp/teamA
        teamChartD[temComINAtrue] = temComp/teamA
        temComINtrue = comp + 'Ratiotrue'
        temCompDict[temComINtrue] = temComp/teamI
        teamChartD[temComINtrue] = temComp/teamI
    ## component whose number is less than 5
        # there needs function like sort to make number sequence??

totalChartDict = {}
#=========================product level==============================
### product level bugs statistic
def CompStatis(prod):
## all bug number
    totalA = prods.find({'product': prod}).count()
    totalBugA[prod] = totalA

## total valid bug number
    totalV = prods.find({'product': prod,'resolution':{'$in': validreso},'severity':{'$ne':'Enhancement'} }).count()
    totalBugV[prod] = totalV

## expend: all valid/ total valid to compare with EBR
    totalValidRatio[prod] = RatioConvert(totalV/totalA)

## component valid bug ratio: component valid/ component total
    totalChartD = totalChartDict.setdefault(prod,{})
    temTotalDict = totalValidComp.setdefault(prod,{})
    for comp in comps:
# component valid
        temVComp = prods.find({'product': prod,'component':comp,'resolution': {'$in':validreso}, 'severity':{'$ne':'Enhancement'} }).count()
# component total
        temAComp = prods.find({'product': prod,'component':comp }).count()
        if temVComp and temAComp:
            temTotalComValid = comp + 'Valid'
            temTotalDict[temTotalComValid ] = temVComp
            temTotalComAll = comp + 'All'
            temTotalDict[temTotalComAll ] = temAComp 
# valid ratio
            temTotalCom = comp + 'Ratio'
            temTotalDict[temTotalCom] = RatioConvert(temVComp/temAComp)
            temTotalComtrue = comp + 'Ratiotrue'
            temTotalDict[temTotalComtrue] = temVComp/temAComp
            totalChartD[temTotalComtrue] = temVComp/temAComp
# valid per component ratio: component valid/ all valid
            temTotalComA = comp + 'InAllRatio'
            temTotalDict[temTotalComA ] = RatioConvert(temVComp/totalV)
            temTotalComAtrue = comp + 'InAllRatiotrue'
            temTotalDict[temTotalComAtrue] = temVComp/totalV
            totalChartD[temTotalComAtrue] = temVComp/totalV
## expend: component valid/ all to compare with EBR
            temTotalComAA = comp + 'ValidInAll'
            temTotalDict[temTotalComAA] = RatioConvert(temVComp/totalA)
       
for product in prod_all:
    EBRStatis(product)
    CompStatis(product)

#=========================Data Statistic Output==============================
#dataPara = ["teamBugA", "teamBugV", "teamValidRatio", "teamInvalidNum", "teamInvalidComp", "totalBugA", "totalBugV", "totalValidRatio", "totalValidComp"]
#dataDc = [teamBugA, teamBugV, teamValidRatio, teamInvalidNum, teamInvalidComp, totalBugA, totalBugV, totalValidRatio, totalValidComp]

def printFD(dicD,item):
    print("\n")
    print(item)
    print("===")
    if isinstance(list(dicD.values())[0],dict):
        print("\n")
        print('product | InvalidType/ Component | BugNum/ Ratio')
        print(':---|---|---')
    else:
        print("\n")
        print('product | Num/ Ratio')
        print(':---|---')
      
    for i in sorted(dicD):
        tmpD = dicD.setdefault(i,dicD[i])
        if isinstance(tmpD,dict):
            for j in sorted(tmpD):
                print('{} | {} | {}'.format(i,j,tmpD[j]))
        else:
            print('{} | {}'.format(i,dicD[i]))

#[printFD(i,dataPara.pop(0)) for i in dataDc]

#=========================Python to chart==============================

pprint(teamChartDict)
pprint(totalChartDict)
#compListTeam = compSelect(teamChartDict)
#compListTotal = compSelect(totalChartDict)

## arg ratio could be 'not' 'Ratio' 'InAllRatio'
def charDFinvT(InPr,InD,InL,ratio):
    N = 6
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars
    
    fig, ax = plt.subplots()
    temColor = ['r','g','y']
    print("inpr: %s" % InPr)
    widthDeta = [width*i for i in range(0,20)]
    rectsL = []
    for i in InPr:
        temL = []
        for j in InL.append(EnhanceSeve):
            if ratio == "not":
                temL.append(InD[i][j])
            else:
                temL.append(InD[i][j+ratio])
        rects = ax.bar(ind+widthDeta.pop(0), temL, width, color=temColor.pop())
        rectsL.append(rects)
    ax.set_ylabel('Bug Number')
#    ax.set_title(lableList.pop(0))
#    ax.set_title("Team invalid type statistic")
    ax.set_xticks(ind+width)
    ax.set_xticklabels( InL )
    
    ax.legend(rectsL, InPr)
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
#    autolabel(rects1)
#    [autolabel(i) for i in rectsL]
    if ratio:
        plt.savefig("InvalidTypeRatio.png")
    else:
        plt.savefig("InvalidType.png")
    
def charDFebr(InPr,AD,VD,picName):
    N = 2
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars
    
    fig, ax = plt.subplots()
    temColor = ['r','g','y']
    widthDeta = [width*i for i in range(0,20)]
    rectsL = []
    for i in InPr:
        temL = [AD[i], VD[i]]
        rects = ax.bar(ind+widthDeta.pop(0), temL, width, color=temColor.pop())
        rectsL.append(rects)
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Bug Number')
#    ax.set_title(lableList.pop(0))
#    ax.set_title("Team invalid type statistic")
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('TeamAllBugs', 'TeamValidBugs'))
    
    ax.legend(rectsL, InPr)
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

#    autolabel(rects1)
#    [autolabel(i) for i in rectsL]
    plt.savefig(picName+".png")

#==================charting output========================
# chart for team valid and all bugs
charDFebr(prod_all,totalBugA,totalBugV,"teamEBR")
# chart for team invalid type/ all bugs
charDFinvT(prod_all,teamInvalidNum,invalidreso,'InAllRatio')
# chart for team invalid component/ all bugs
charDFinvT(prod_all,teamInvalidComp,compListTeam,'InAllRatio')

# chart for total valid and all bugs
charDFebr(prod_all,totalBugA,totalBugV,"totalEBR")
# chart for total valid component/ all bugs
charDFinvT(prod_all,totalValidComp,compListTotal,'InAllRatio')
