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

from core import *

class Chart(DIV):
    
    RATIO_1 = ATTR(**{'ratio' : '1:1'})
    RATIO_2 = ATTR(**{'ratio' : '2:1'})
    RATIO_3 = ATTR(**{'ratio' : '3:1'})
    RATIO_4 = ATTR(**{'ratio' : '4:1'})
    RATIO_5 = ATTR(**{'ratio' : '5:1'})
    RATIO_6 = ATTR(**{'ratio' : '6:1'})
    RATIO_7 = ATTR(**{'ratio' : '7:1'})
    RATIO_8 = ATTR(**{'ratio' : '8:1'})
    RATIO_9 = ATTR(**{'ratio' : '9:1'})
    RATIO_A = ATTR(**{'ratio' : '10:1'})
    RATIO_B = ATTR(**{'ratio' : '11:1'})
    RATIO_C = ATTR(**{'ratio' : '12:1'})
    
    XSLEGEND = ATTR(**{'legend' : {'labels' : {'boxWidth' : 10, 'fontSize' : 8, 'padding' : 5}}})
    NOLEGEND = ATTR(**{'legend' : {'display' : False}})
    SCALE100 = ATTR(**{'scales' : {'yAxes' : [{'ticks' : {'min' : 0, 'max' : 100}}]}})
    NOXLABEL = ATTR(**{'scales' : {'xAxes' : [{'display' : False}]}})
    NOXLY100 = ATTR(**{'scales' : {'yAxes' : [{'ticks' : {'min' : 0, 'max' : 100}}], 'xAxes' : [{'display' : False}]}})
    
    def __init__(self, _type, *labels, **options):
        if 'ratio' in options:
            ratio = options.pop('ratio').split(':')
            ratioW = ratio[0]
            ratioH = ratio[1]
        else:
            ratioW = '1'
            ratioH = '1'
        DIV.__init__(self, **{'class' : 'chartwrapper'})
        self.datasets = []
        canvas = VIEW('CANVAS', **{'id' : VIEW.getUUID(), 'lib' : 'chartjs', 'width' : ratioW, 'height' : ratioH})
        canvas['chart'] = {
            'type' : _type,
            'data' : {'labels' : labels, 'datasets' : self.datasets},
            'options' : options
            }
        self.html(canvas)
    
class Line(Chart):
    
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'line', *labels, **options)
        self.rgb = RGB()
    
    def Data(self, label, *data, **desc):
        desc['label'] = label
        desc['data'] = data
        rgb = self.rgb.getNext()
        if 'borderColor' not in desc: desc['borderColor'] = 'rgba(%d,%d,%d,1)' % rgb
        if 'backgroundColor' not in desc: desc['backgroundColor'] = 'rgba(%d,%d,%d,0.3)' % rgb
        self.datasets.append(desc)
        return self

class Bar(Chart):
    
    LABEL = ATTR(**{'colortype' : 'label'})
    DATA = ATTR(**{'colortype' : 'data'})
    
    def __init__(self, *labels, **options):
        if 'colortype' in options: self.colortype = options.pop('colortype')
        else: self.colortype = 'label'
        if self.colortype == 'label':
            rgb = RGB()
            self.bdcolors = []
            self.bgcolors = []
            for l in labels:
                color = rgb.getNext()
                self.bdcolors.append('rgba(%d,%d,%d,1)' % color)
                self.bgcolors.append('rgba(%d,%d,%d,0.8)' % color)
        else: self.rgb = RGB()
        Chart.__init__(self, 'bar', *labels, **options)
    
    def Data(self, label, *data, **desc):
        desc['label'] = label
        desc['data'] = data
        if self.colortype == 'label':
            if 'borderColor' not in desc: desc['borderColor'] = self.bdcolors
            if 'backgroundColor' not in desc: desc['backgroundColor'] = self.bgcolors
        else:
            rgb = self.rgb.getNext()
            if 'borderColor' not in desc: desc['borderColor'] = 'rgba(%d,%d,%d,1)' % rgb
            if 'backgroundColor' not in desc: desc['backgroundColor'] = 'rgba(%d,%d,%d,0.8)' % rgb
        self.datasets.append(desc)
        return self

class HealthBar(Chart):
    
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'bar', *labels, **(Chart.NOLEGEND + options))

    def Data(self, label, *data, **desc):
        desc['label'] = label
        desc['data'] = data
        bdcolors = []
        bgcolors = []
        for d in data:
            if d == None:
                bdcolors.append('rgba(0,0,0,1)')
                bgcolors.append('rgba(0,0,0,0.8)')
            else:
                r = 255 - int( ( 0.01 * d ) * 255 )
                g = int( ( 0.01 * d ) * 255 )
                bdcolors.append('rgba(%d,%d,0,1)' % (r, g))
                bgcolors.append('rgba(%d,%d,0,0.8)' % (r, g))
        desc['borderColor'] = bdcolors
        desc['backgroundColor'] = bgcolors
        desc['borderWidth'] = 1
        self.datasets.append(desc)
        return self

class Pie(Chart):
    
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'pie', *labels, **options)
        rgb = RGB()
        self.bdcolors = []
        self.bgcolors = []
        for l in labels:
            color = rgb.getNext()
            self.bdcolors.append('rgba(%d,%d,%d,1)' % color)
            self.bgcolors.append('rgba(%d,%d,%d,0.8)' % color)
        
    def Data(self, label, *data, **desc):
        desc['label'] = label
        desc['data'] = data
        if 'borderColor' not in desc: desc['borderColor'] = self.bdcolors
        if 'backgroundColor' not in desc: desc['backgroundColor'] = self.bgcolors
        self.datasets.append(desc)
        return self

class Donut(Chart):
    
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'doughnut', *labels, **options)
        rgb = RGB()
        self.bdcolors = []
        self.bgcolors = []
        for l in labels:
            color = rgb.getNext()
            self.bdcolors.append('rgba(%d,%d,%d,1)' % color)
            self.bgcolors.append('rgba(%d,%d,%d,0.8)' % color)
        
    def Data(self, label, *data, **desc):
        desc['label'] = label
        desc['data'] = data
        if 'borderColor' not in desc: desc['borderColor'] = self.bdcolors
        if 'backgroundColor' not in desc: desc['backgroundColor'] = self.bgcolors
        self.datasets.append(desc)
        return self
