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

import uuid

class VIEW(dict):
    
    @classmethod
    def getUUID(cls): return str(uuid.uuid4())
    
    @classmethod
    def setAttrs(cls, kv, attrs):
        for key in kv: attrs[key] = kv[key] + ' ' + attrs[key] if key in attrs else kv[key]
    
    def __init__(self, _type, **attrs):
        dict.__init__(self, type=_type, elements=[], attrs=attrs)
        
    def html(self, element):
        self['elements'].append(element)
        return self
    
    def __len__(self, *args, **kwargs):
        return self['elements'].__len__()
    
    def isEmpty(self):
        return not self.__len__()
    
class DIV(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'div', **attrs)

class SPAN(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'span', **attrs)

class HEAD(VIEW):
    def __init__(self, level, **attrs):
        VIEW.__init__(self, 'h' + str(level), **attrs)

class PARA(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'p', **attrs)

class ANCH(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'a', **attrs)

class LABEL(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'label', **attrs)

class TABLE(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'table', **attrs)
        
class THEAD(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'thead', **attrs)
        
class TBODY(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'tbody', **attrs)
        
class TH(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'th', **attrs)
        
class TR(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'tr', **attrs)

class TD(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'td', **attrs)
        
class UL(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'ul', **attrs)

class LI(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'li', **attrs)

class FORM(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'form', **attrs)

class INPUT(VIEW):
        def __init__(self, **attrs):
            VIEW.__init__(self, 'input', **attrs)

class BUTTON(VIEW):
    def __init__(self, **attrs):
        VIEW.setAttrs({'class' : 'btn', 'type' : 'button'}, attrs)
        VIEW.__init__(self, 'button', **attrs)
