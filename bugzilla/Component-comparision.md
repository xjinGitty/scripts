Product level bugs data comparison statistics
===



    Products: SLED11SP3/ SLED12/ SLED11SP4  
    Representor: Xiaojun Jin (with Xudong zhang's great support:)
    Due Date: 2015-07-31    

Notes and Formula:
===
+ valid: bugs(exclude whose status is ENHANCEMENT-DPLICATED-INVALID-WONTFIX-WORKSFORME)
+ valid bug report rate: component valid bugs number /component all bugs number
+ component bug report rate: component valid bugs number /sum of all component valid bugs number

words at the beginning:
===
The product level comparison (sled11sp4 vs sled12 vs sled11sp3), could have 2 perspectives (formula as above):
1. the statistics of each components' valid bug report rate 
2. the statistics of each components' component bug report rate

        First we statistic the 2 group data for bugs reported by all colleagues.

        Then we change the data range, that means we just pick bugs that reported by our teammates, and calculate the 2 group data use the same method as above.

        The purpose of we made our team's bug reporting status statistics is that, through the statistic we could see our test points  and where we differ with other QA colleagues and we also could see our workload, how about our work's efficiency.    
    
    ---------

+ demonstration for valid bug number/ total bug number -> EBR in product lever
![](https://github.com/xjinGitty/scripts/blob/master/bugzilla/totalallandvalidnumber.png?raw=true)

+ demonstration for each component's valid bug number/ total valid bug number
![](https://github.com/xjinGitty/scripts/blob/master/bugzilla/totalcompvalidinallvalid.png?raw=true)

+ demonstration for each component's valid bug number/ component's total bug number
![](https://github.com/xjinGitty/scripts/blob/master/bugzilla/totalcompvalidincompall.png?raw=true)


Reference:
===
script could be found at: 
https://github.com/xjinGitty/scripts/blob/master/bugzilla/QualityMetrics-running.py

