# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:41:10 2022

@author: ScottStation
"""


import qesdk2
import sys
import platform

from datetime import datetime,timedelta

def get_mac_address():
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8],mac[8:10], mac[10:])

def get_ver():
    vers= sys.version.split('.')
    return '_'.join(vers[:2])

def get_plat():
    return platform.system().lower()

qesdk2.auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')

df = qesdk2.get_product_invent_orders('CU', '2023-02-01','2023-02-14')
print(df)
#msg = qesdk2.get_package_address('algoex', get_plat(), get_ver(), get_mac_address())
#print(msg)
#print(qesdk2.get_plugin_permission('algoex','windows','3_8',get_mac_address(),'test','quantease'))
#df = qesdk.get_price('AG2212.SFE','2022-10-01','2022-11-01','daily')
#print(df)
#qesdk2.auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')

#print(qesdk2.get_broker_info('cjqh3'))
#print(qesdk2.get_valid_instID('si9w'))#
#print(qesdk2.is_valid_instID('IC2309.SFE'))
#print(qesdk2.is_valid_trade_time('IC2306.SFE',datetime.now()+timedelta(hours=5)))
#df = qesdk.get_realtime_minute_prices(['AU2212_SFE','AG2301.SFE'])
#print(df)
'''
testdf = qesdk.get_bar_data(['AU2212.SFE'],'2022-12-06')
for i in testdf['AU2212.SFE'].index:
    print(testdf['AU2212.SFE'].loc[i,'time'],testdf['AU2212.SFE'].loc[i, 'close'])
testdf['AU2212.SFE']['close'].plot()    
'''