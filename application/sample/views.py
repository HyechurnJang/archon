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
    
    chart = Chart.Line
    
    V.Page.html(chart(*labels).Data('Line1', *data3))
    
    V.Page.html(chart(*labels, **options1).Data('Line1', *data3))
    V.Page.html(chart(*labels, **options2).Data('Line1', *data3))
    
    V.Page.html(chart(*labels, **Chart.THEME_HEALTH).Data('Line1', *data3))
    V.Page.html(chart(*labels, **Chart.THEME_UTIL).Data('Line1', *data3))
    
    V.Page.html(chart(*labels).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    
    V.Page.html(chart(*labels, **options1).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    V.Page.html(chart(*labels, **options2).Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3))
    
@pageview(Manager)
def peity(R, M, V):
    
    V.Page.html(
        DIV().html(
            Figure.Line(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200),
            Figure.Bar(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200),
            Figure.Pie(1,5, height=100, width=100),
            Figure.Donut(1,5, height=100, width=100)
        )
    )
    
    V.Page.html(
        DIV().html(
            Figure.Line(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200, **Figure.THEME_HEALTH),
            Figure.Bar(*[100, 4, 20, 50, 70, 10, 30], height=100, width=200, **Figure.THEME_UTIL),
            Figure.Pie(20, 80, height=100, width=100, color=Figure.COLOR_HEALTH),
            Figure.Donut(20, 80, height=100, width=100, color=Figure.COLOR_UTIL)
        )
    )
    
    V.Page.html(
        DIV().html(
            Figure.Pie(0, 100, height=100, width=100, **Figure.THEME_HEALTH),
            Figure.Pie(25, 75, height=100, width=100, **Figure.THEME_HEALTH),
            Figure.Pie(50, 50, height=100, width=100, **Figure.THEME_HEALTH),
            Figure.Pie(75, 25, height=100, width=100, **Figure.THEME_HEALTH),
            Figure.Pie(100, 0, height=100, width=100, **Figure.THEME_HEALTH),
        )
    )
    
    V.Page.html(
        DIV().html(
            Figure.Donut(0, 100, height=100, width=100, hole=10, **Figure.THEME_UTIL),
            Figure.Donut(25, 75, height=100, width=100, hole=20, **Figure.THEME_UTIL),
            Figure.Donut(50, 50, height=100, width=100, **Figure.THEME_UTIL),
            Figure.Donut(75, 25, height=100, width=100, **Figure.THEME_UTIL),
            Figure.Donut(100, 0, height=100, width=100, **Figure.THEME_UTIL),
        )
    )

@pageview(Manager)
def arbor(R, M, V):
    
    topo = Topo(height=0)
    
    topo.Node('Test1', 'Test1OK')
    topo.Node('Test2', 'Test2')
    topo.Edge('Test1', 'Test2')
    
    V.Page.html(topo)

@pageview(Manager)
def justgage(R, M, V):
    
    V.Page.html(
'''
<div>
<div id="test-justgage">
</div>
</div>
<script language="javascript" type="text/javascript">
setTimeout(function() {
    var g = new JustGage({
        id: "test-justgage",
        title: "Test JustGage,
        value: getRandomInt(0, 100),
        min: 0,
        max: 100,
        pointer: true,
        pointerOptions: {
            toplength: -15,
            bottomlength: 10,
            bottomwidth: 12,
            color: '#8e8e93',
            stroke: '#ffffff',
            stroke_width: 3,
            stroke_linecap: 'round'
        }
    });
}, 250);
</script>
'''
    )
    
    gauge = Gauge('Test1', 40)
    V.Page.html(gauge)

@pageview(Manager)
def html(request, manager, view):
    
    pass
