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
def chartjs(request, manager, view):
    labels = ['A', 'B', 'C']
    data1 = [None, 10, 50]
    data2 = [30, 2, 100]
    data3 = [70, None, 0]
    
    line = Line(*labels, **(Chart.SCALE100 + Chart.RATIO41))
    line.Data('Line1', *data1).Data('Line2', *data2).Data('Line3', *data3)
    view.Page.html(line)
    
    bar1 = Bar(*labels, **(Chart.SCALE100 + Chart.RATIO41 + Bar.LABEL))
    bar1.Data('Bar1', *data1).Data('Bar2', *data2).Data('Bar3', *data3)
    view.Page.html(bar1)
    
    bar2 = Bar(*labels, **(Chart.SCALE100 + Chart.RATIO41 + Bar.DATA))
    bar2.Data('Bar1', *data1).Data('Bar2', *data2).Data('Bar3', *data3)
    view.Page.html(bar2)
    
    bar3 = Bar(*labels, **(Chart.SCALE100 + Chart.RATIO41 + Bar.LABEL))
    bar3.Data('Bar1', *data2)
    view.Page.html(bar3)
    
    bar4 = Bar(*labels, **(Chart.SCALE100 + Chart.RATIO41 + Bar.DATA))
    bar4.Data('Bar1', *data2)
    view.Page.html(bar4)
    
    hbar = HealthBar(*labels, **(Chart.SCALE100 + Chart.RATIO41))
    hbar.Data('Bar1', *data1).Data('Bar2', *data2).Data('Bar3', *data3)
    view.Page.html(hbar)
    
    pie = Pie(*labels, **(Chart.RATIO31))
    pie.Data('Pie1', *data1).Data('Pie2', *data2).Data('Pie3', *data3)
    view.Page.html(pie)
    
    nut1 = Donut(*labels, **(Chart.RATIO31))
    nut1.Data('Donut1', *data1).Data('Donut2', *data2).Data('Donut3', *data3)
    view.Page.html(nut1)
    
    nut2 = Donut(*labels, **(Chart.RATIO31))
    nut2.Data('Donut1', *data2)
    view.Page.html(nut2)
    
@pageview(Manager)
def nextui(request, manager, view):
    
    topo = NextTopo().Node('jang', 'Jang', 100, 200).Node('hye', 'Hye', 200, 200).Node('churn', 'Churn', 300, 300)
    topo.Link('jang', 'hye').Link('hye', 'churn').Link('churn', 'jang')
    
    view.Page.html(topo)

@pageview(Manager)
def sigmajs(request, manager, view):
    
    topo = SigmaJS().Node('jang', 'Jang', 0, 0, 5).Node('hye', 'Hye', 3, 1, 2).Node('churn', 'Churn', 1, 3, 1).Node('geni', 'Geni', 4, 4, 4)
    topo.Edge('jh', 'jang', 'hye').Edge('hc', 'hye', 'churn').Edge('cj', 'churn', 'jang').Edge('gj', 'geni', 'jang')
    view.Page.html(topo)

@pageview(Manager)
def html(request, manager, view):
    
    nt = NavTab()
    
    nt.Tab('Jang', HEAD(3).html('Jang'))
    nt.Tab('Hye', HEAD(3).html('Hye'))
    nt.Tab('Churn', HEAD(3).html('Churn'))
    
    view.Page.html(nt)
    
    view.Page.html('''

<ul class="nav nav-tabs" role="tablist">
    <li role="presentation"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">Home</a></li>
    <li role="presentation"><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Profile</a></li>
    <li role="presentation"><a href="#messages" aria-controls="messages" role="tab" data-toggle="tab">Messages</a></li>
    <li role="presentation"><a href="#settings" aria-controls="settings" role="tab" data-toggle="tab">Settings</a></li>
</ul>

<div class="tab-content">
    <div role="tabpanel" class="tab-pane active" id="home">Home</div>
    <div role="tabpanel" class="tab-pane" id="profile">Profile</div>
    <div role="tabpanel" class="tab-pane" id="messages">Messages</div>
    <div role="tabpanel" class="tab-pane" id="settings">Settings</div>
</div>

''')