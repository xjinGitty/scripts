#! /usr/bin/python3

from pymongo import MongoClient
client = MongoClient('mongodb://147.2.212.204:27017/')
prods = client.bz.prods


prod_all = [  'SUSE Linux Enterprise Desktop 12',
              'SUSE Linux Enterprise Desktop 11 SP3',
              'SUSE Linux Enterprise Desktop 11 SP4 (SLED 11 SP4)']

bug_sts = ['---','FIXED','UPSTREAM','NORESPONSE','MOVED','INVALID','WONTFIX','DUPLICATE','FEATURE','WORKSFORME']

#def allBug(prod_all):
#    for prod in prod_all:
#        bugTeam+"${prod}" = prods.find({'product': "${prod}",'creator': {'$in': ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com','ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com','yosun@suse.com','nwang@suse.com','bchou@suse.com']} })
#        print ${prod}
#        print bugTeam+"${prod}"
teamBugA = {}
totalBugA = {}
teamBugV = {}
totalBugV = {}

for prod in prod_all:
    teamA = prods.find({'product': prod,'creator': {'$in': ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com','ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com','yosun@suse.com','nwang@suse.com','bchou@suse.com']} }).count()
    teamBugA[prod] = teamA

    totalA = prods.find({'product': prod,'cf_foundby': '---'}).count()
    totalBugA[prod] = totalA

    teamV = prods.find({'product': prod,'creator': {'$in': ['xdzhang@suse.com', 'xjin@suse.com','yfjiang@suse.com','ychen@suse.com','ysun@suse.com','wjiang@suse.com','whdu@suse.com','sywang@suse.com','yosun@suse.com','nwang@suse.com','bchou@suse.com']},'resolution':{'$in':['FIXED','UPSTEAM','NORESPONSE','---','MOVED']},'severity':{'$ne':'Enhancement'} }).count()
    teamBugV[prod] = teamV

    totalV = prods.find({'product': prod,'cf_foundby': '---','resolution':{'$in':['FIXED','UPSTEAM','NORESPONSE','---','MOVED']},'severity':{'$ne':'Enhancement'} }).count()
    totalBugV[prod] = totalV


print("num of total bugs reported by QA APACI is:" + str(teamBugA))
print("num of total bugs reported by all QA colleague is:" + str(teamBugA))
print("num of valid bugs reported by QA APACI is:" + str(teamBugA))
print("num of valid bugs reported by all QA colleague is:" + str(teamBugA))
# format print
'num of total bugs reported by QA APACI is: {0}'


#pxeitem = 'LABEL {0}\n' \
#          '    MENU LABEL {0}\n' \
#          '    KERNEL {1}linux\n' \
#          '    APPEND initrd={1}initrd install={2}\n'.format(
#                  label, ploader, repo)


