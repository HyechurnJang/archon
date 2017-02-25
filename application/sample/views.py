# -*- coding: utf-8 -*-
################################################################################
#        _____ _                  _____           _                            #
#       / ____(_)                / ____|         | |                           #
#      | |     _ ___  ___ ___   | (___  _   _ ___| |_ ___ _ __ ___  ___        #
#      | |    | / __|/ __/ _ \   \___ \| | | / __| __/ _ \ '_ ` _ \/ __|       #
#      | |____| \__ \ (_| (_) |  ____) | |_| \__ \ ||  __/ | | | | \__ \       #
#       \_____|_|___/\___\___/  |_____/ \__, |___/\__\___|_| |_| |_|___/       #
#                                        __/ |                                 #
#                                       |___/                                  #
#           _  __                       _____       _  _____ ______            #
#          | |/ /                      / ____|     | |/ ____|  ____|           #
#          | ' / ___  _ __ ___  __ _  | (___   ___ | | (___ | |__              #
#          |  < / _ \| '__/ _ \/ _` |  \___ \ / _ \| |\___ \|  __|             #
#          | . \ (_) | | |  __/ (_| |  ____) | (_) | |____) | |____            #
#          |_|\_\___/|_|  \___|\__,_| |_____/ \___/|_|_____/|______|           #
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2016 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
# Licensed under the Apache License, Version 2.0 (the "License"); you may      #
# not use this file except in compliance with the License. You may obtain      #
# a copy of the License at                                                     #
#                                                                              #
# http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################

from archon import *
from manager import Manager

#===============================================================================
# Create your views here.
#===============================================================================

@pageview(Manager)
def core(R, M, V):
    
    pass

@pageview(Manager)
def deco(R, M, V):
    
    pass

@pageview(Manager)
def action(R, M, V):
    
    pass

table_data1 = [
    ["Airi","Satou","Accountant","Tokyo","28th Nov 08","$162,700"],
    ["Angelica","Ramos","Chief Executive Officer (CEO)","London","9th Oct 09","$1,200,000"],
    ["Ashton","Cox","Junior Technical Author","San Francisco","12th Jan 09","$86,000"],
    ["Bradley","Greer","Software Engineer","London","13th Oct 12","$132,000"],
    ["Brenden","Wagner","Software Engineer","San Francisco","7th Jun 11","$206,850"],
    ["Brielle","Williamson","Integration Specialist","New York","2nd Dec 12","$372,000"],
    ["Bruno","Nash","Software Engineer","London","3rd May 11","$163,500"],
    ["Caesar","Vance","Pre-Sales Support","New York","12th Dec 11","$106,450"],
    ["Cara","Stevens","Sales Assistant","New York","6th Dec 11","$145,600"],
    ["Cedric","Kelly","Senior Javascript Developer","Edinburgh","29th Mar 12","$433,060"]
]

table_data2 = [
    [STRONG().html("airi"),"satou","Accountant","Tokyo","28th Nov 08","$162,700"],
    [PARA().html(SMALL().html("angelica"), STRONG().html('!!!')),"ramos","Chief Executive Officer (CEO)","London","9th Oct 09","$1,200,000"],
    [GET('/sample/samples/table').html("ashton"),"cox","Junior Technical Author","San Francisco","12th Jan 09","$86,000"],
    ["bradley","greer","Software Engineer","London","13th Oct 12","$132,000"],
    ["brenden","wagner","Software Engineer","San Francisco","7th Jun 11","$206,850"],
    ["brielle","williamson","Integration Specialist","New York","2nd Dec 12","$372,000"],
    ["bruno","nash","Software Engineer","London","3rd May 11","$163,500"],
    ["caesar","vance","Pre-Sales Support","New York","12th Dec 11","$106,450"],
    ["cara","stevens","Sales Assistant","New York","6th Dec 11","$145,600"],
    ["cedric","kelly","Senior Javascript Developer","Edinburgh","29th Mar 12","$433,060"]
]

@TABLE.ASYNC.pageview()
def sub_table(R, M, V):
    print 'Draw   :', R.Draw
    print 'Leng   :', R.Length
    print 'Start  :', R.Start
    print 'Search :', R.Search
    print 'OrderC :', R.OrderCol
    print 'OrderD :', R.OrderDir
    
    total = 57
    count = 47
    
    ret = TABLE.ASYNCDATA(R.Draw, total, count)
    if R.Start == 0:
        for td in table_data1: ret.Record(*td)
    else:
        for td in table_data2: ret.Record(*td) 
    
    return ret

@pageview(Manager, sub_table=sub_table)
def table(R, M, V):
    
    basic = TABLE.BASIC('First Name', 'Last Name', 'Position', 'Office', 'Start Data', 'Salary')
    for record in table_data1: basic.Record(*record)
    V.Page.html(basic)
    
    asyn = TABLE.ASYNC('sample/samples/table/sub_table', 'First Name', 'Last Name', 'Position', 'Office', 'Start Data', 'Salary')
    V.Page.html(asyn)
     
    flip = TABLE.FLIP('First Name', 'Last Name', '+Position', '+Office', '+Start Data', 'Salary')
    for record in table_data1: flip.Record(*record)
    V.Page.html(flip)

@pageview(Manager)
def dimple(R, M, V):
    
    labels = ['A', 'B', 'C', 'D']
    data1 = [None, 10, 30, 90]
    data2 = [30, 2, 100, 20]
    data3 = [70, None, 80, 50]
    
    options1 = {
        'pivot' : True,
        'stack' : True,
        'xkey' : 'Category',
        'ykey' : 'Value',
        'legend' : True,
    }
    
    options2 = {
        'legend' : True,
    }
    
    chart = CHART.LINE
    
    V.Page.html(chart(*labels).Data('Line1', *data3))
    
    V.Page.html(chart(*labels, **options1).Data('Line1', *data3))
    V.Page.html(chart(*labels, **options2).Data('Line1', *data3))
    
    V.Page.html(chart(*labels, **CHART.THEME_HEALTH).Data('Line1', *data3))
    V.Page.html(chart(*labels, **CHART.THEME_UTIL).Data('Line1', *data3))
    
    V.Page.html(chart(*labels).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    
    V.Page.html(chart(*labels, **options1).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    V.Page.html(chart(*labels, **options2).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    
@pageview(Manager)
def peity(R, M, V):
    
    V.Page.html(
        DIV().html(
            FIGURE.LINE(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200),
            FIGURE.BAR(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200),
            FIGURE.PIE(1,5, height=100, width=100),
            FIGURE.DONUT(1,5, height=100, width=100)
        )
    )
    
    V.Page.html(
        DIV().html(
            FIGURE.LINE(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200, **FIGURE.THEME_HEALTH),
            FIGURE.BAR(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200, **FIGURE.THEME_UTIL),
            FIGURE.PIE(20, 80, height=100, width=100, color=FIGURE.COLOR_HEALTH),
            FIGURE.DONUT(20, 80, height=100, width=100, color=FIGURE.COLOR_UTIL)
        )
    )
    
    V.Page.html(
        DIV().html(
            FIGURE.PIE(0, 100, height=100, width=100, **FIGURE.THEME_HEALTH),
            FIGURE.PIE(25, 75, height=100, width=100, **FIGURE.THEME_HEALTH),
            FIGURE.PIE(50, 50, height=100, width=100, **FIGURE.THEME_HEALTH),
            FIGURE.PIE(75, 25, height=100, width=100, **FIGURE.THEME_HEALTH),
            FIGURE.PIE(100, 0, height=100, width=100, **FIGURE.THEME_HEALTH),
        )
    )
    
    V.Page.html(
        DIV().html(
            FIGURE.DONUT(0, 100, height=100, width=100, hole=10, **FIGURE.THEME_UTIL),
            FIGURE.DONUT(25, 75, height=100, width=100, hole=20, **FIGURE.THEME_UTIL),
            FIGURE.DONUT(50, 50, height=100, width=100, **FIGURE.THEME_UTIL),
            FIGURE.DONUT(75, 25, height=100, width=100, **FIGURE.THEME_UTIL),
            FIGURE.DONUT(100, 0, height=100, width=100, **FIGURE.THEME_UTIL),
        )
    )

@pageview(Manager)
def arbor(R, M, V):
    
    topo = TOPO(height=0)
    
    topo.Node('Test1', 'Test1OK')
    topo.Node('Test2', 'Test2')
    topo.Edge('Test1', 'Test2')
    
    V.Page.html(topo)

@pageview(Manager)
def justgage(R, M, V):
    gauge = GAUGE('Test1', 40)
    V.Page.html(gauge)

@pageview(Manager)
def html(R, M, V):

    pass