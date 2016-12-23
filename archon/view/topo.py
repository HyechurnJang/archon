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

class SigmaJS(VIEW):
    
    def __init__(self, **options):
        VIEW.__init__(self, 'DIV', **{'id' : VIEW.getUUID(), 'class' : 'chartwrapper', 'lib' : 'sigmajs'})
        self.nodes = []
        self.edges = []
        self['chart'] = {
            'nodes' : self.nodes,
            'edges' : self.edges
            }
    
    def Node(self, id, label, x, y, size):
        self.nodes.append({'id' : id, 'label' : label, 'x' : x, 'y' : y, 'size' : size})
        return self

    def Edge(self, id, src, dst):
        self.edges.append({'id' : id, 'source' : src, 'target' : dst})
        return self 

class NextTopo(VIEW):
    
    def __init__(self, **options):
        VIEW.__init__(self, 'DIV', **{'id' : VIEW.getUUID(), 'class' : 'chartview', 'lib' : 'nextui'})
        self.nodes = []
        self.links = []
        self['chart'] = {
            'nodes' : self.nodes,
            'links' : self.links
            }
    
    def Node(self, id, name, x, y):
        self.nodes.append({'id' : id, 'name' : name, 'x' : x, 'y' : y})
        return self

    def Link(self, src, dst):
        self.links.append({'source' : src, 'target' : dst})
        return self