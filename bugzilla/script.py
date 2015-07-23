#! /usr/bin/python3
from pprint import pprint
from pymongo import MongoClient
client = MongoClient('mongodb://147.2.212.204:27017/')
prods = client.bz.prods

# all data structure
prod_all = [  'SUSE Linux Enterprise Desktop 12',
              'SUSE Linux Enterprise Desktop 11 SP3',
              'SUSE Linux Enterprise Desktop 11 SP4 (SLED 11 SP4)']

teamMem = ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com','ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com','yosun@suse.com','nwang@suse.com','bchou@suse.com']

validreso = ['FIXED','UPSTEAM','NORESPONSE','---','MOVED']
invalidreso = ['INVALID','WONTFIX','DUPLICATE','FEATURE','WORKSFORME']

comp = prods.find({})
comp = [i['component'] for i in comp]
comps = set(comp)
#### component excludes
#### query range shrink
#### 

### EBR specific data structure
teamBugA = {}
teamBugV = {}
teamValidRatio = {}
teamInvalidNum = {}
teamInvalidComp = {}

### product level specific data structure
totalBugA = {}
totalBugV = {}
totalValidRatio = {}
totalValidComp = {}

for prod in prod_all:
#======================EBR data==========================
### EBR related statistic: we just consider for bugs reported by QA APACI
## all bug number
    tmp = prods.find({'product': prod,'creator': {'$in':teamMem} }).count()
    teamBugA[prod] = tmp 

## valid bug number
    TVratio = prods.find({'product': prod,'creator': {'$in': teamMem},'resolution':{'$in': validreso},'severity':{'$ne':'Enhancement'} }).count()
    teamBugV[prod] = tmp 

## EBR ratio
#    TVratio = $((teamV/teamA))
    teamValidRatio[prod] = TVratio

## invalid bug number statistic
# all invalid bug number
#    teamI = $((teamA - teamV))
# INVALID # WONTFIX # DUPLICATE # WORKSFORME # bug num
    tmpDict = teamInvalidNum.setdefault(prod, {})
    for reso in invalidreso:
        tmp = prods.find({'product': prod,'creator': {'$in': teamMem},'resolution':reso}).count()
        tmpDict[reso] = tmp
#== each invalid type/all ratio??==#== each invalid type/all invalid ratio??
        tmpTypeRatio = reso+'InAllratio'
#        tmpDict[tmpTypeRatio] = $((tmp/teamA))
        temInvalidRatio = reso+'InAllInvalidRatio'
#        tmpDict[temInvalidRatio] = $((tmp/teamI))
## ENHANCEMENT
    temEnhance = prods.find({'product': prod,'creator': {'$in': teamMem},'severity':'Enhancement'}).count()
    tmpDict['EnhanceSeve'] = temEnhance
#    tmpDict['EnhanceSeveAllRatio'] = $((temEnhance/teamA))
#    tmpDict['EnhanceSeveInvalidRatio'] = $((temEnhance/teamI))

## each component invalid/ total invalid ratio
    temCompDict = teamInvalidComp.setdefault(prod,{})
    for comp in comps:
        temComp = prods.find({'product': prod,'creator': {'$in': teamMem},'component':comp,'resolution': {'$in':invalidreso}, 'severity':'Enhancement' }).count()
        temCompDict[comp] = temComp
        temComIN = comp + 'inAllInvalidRatio'
#        temCompDict[temComIN] = $((temComp/teamI))
## component whose number is less than 5
    # there needs function like sort to make number sequence??

#=========================product level==============================
### product level bugs statistic
## all bug number
    totalA = prods.find({'product': prod}).count()
    totalBugA[prod] = totalA

## total valid bug number
    totalV = prods.find({'product': prod,'resolution':{'$in': validreso},'severity':{'$ne':'Enhancement'} }).count()
    totalBugV[prod] = totalV

## expend: all valid/ total valid to compare with EBR
#    totalValidRatio[prod] = $((totalV/totalA))

## component valid bug ratio: component valid/ component total
    temTotalDict = totalValidComp.setdefault(prod,{})
    for comp in comps:
# component valid
        temVComp = prods.find({'product': prod,'component':comp,'resolution': {'$in':validreso}, 'severity':{'$ne':'Enhancement'} }).count()
        temTotalDict[comp] = temVComp
# component total
        temAComp = prods.find({'product': prod,'component':comp }).count()
        temTotalComAll = comp + 'All'
        temTotalDict[temTotalComAll ] = temAComp 
# valid ratio
        temTotalCom = comp + 'validRatio'
#        temTotalDict[temTotalCom] = $((temVComp/temAcomp))
# valid per component ratio: component valid/ all valid
        temTotalComA = comp + 'inAllValid'
#        temTotalDict[temTotalComA ] = $((temVComp/totalV))
## expend: component valid/ all to compare with EBR
        temTotalComAA = comp + 'inAll'
#        temTotalDict[temTotalComAA] = $((temVComp/totalA))

# format print
'num of total bugs reported by QA APACI is: {0}'


#                pxeitem = 'LABEL {0}\n' \
#                          '    MENU LABEL {0}\n' \
#                          '    KERNEL {1}linux\n' \
#                          '    APPEND initrd={1}initrd install={2}\n'.format(
#                                  label, ploader, repo)

print(str(teamBugA))
print(str(teamBugV))
print(str(teamValidRatio))
print(str(teamInvalidNum))
print(str(totalBugA))
print(str(totalBugV))
print(str(totalValidRatio))
print(str(totalValidComp))
print(str(teamInvalidComp))

pprint(totalValidComp)
