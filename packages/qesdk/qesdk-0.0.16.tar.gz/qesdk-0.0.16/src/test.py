# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:41:10 2022

@author: ScottStation
"""


import qesdk
qesdk.auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')
print(qesdk.check_auth())
'''
qesdk.login('scott','12345678')
stratlist=(qesdk.sm_get_clone_strat_list())
print('strats',stratlist)
if stratlist and isinstance(stratlist,list) and len(stratlist) > 0:
    print(qesdk.sm_get_clone_strat_position(stratlist))
'''
df = qesdk.get_product_invent_orders('CU', '2023-02-01','2023-02-14')
print(df)
    
#qesdk.auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')
#df = qesdk.get_realtime_minute_prices(['AU2212.SFE','AG2301.SFE'])
#print(df)
#print(qesdk2.get_price('AG2212.SFE','2022-09-01','2022-09-22'))