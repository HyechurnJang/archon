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
    def getUUID(cls): return 'A-' + str(uuid.uuid4())
    
    def __init__(self, _type, **attrs):
        dict.__init__(self, type=_type, elements=[], attrs=attrs)
    
    def __len__(self, *args, **kwargs):
        return self['elements'].__len__()
        
    def html(self, *elements):
        for element in elements: self['elements'].append(element)
        return self
    
    def isEmpty(self):
        return not self.__len__()

class ATTR(dict):
    
    @classmethod
    def merge(cls, a1, a2):
        ret = ATTR(**a2)
        for key in a1: ret[key] = ret[key] + ' ' + a1[key] if key in ret else a1[key]
        return ret
    
    @classmethod
    def click(cls, url):
        return ATTR(**{'onclick' : "GetData('%s');" % url}) 
    
    def __init__(self, **attrs):
        dict.__init__(self, **attrs)
        
    def __add__(self, attr):
        return ATTR(**dict(self.items() + attr.items()))
    
    def __lshift__(self, attr):
        for key in attr: self[key] = self[key] + ' ' + attr[key] if key in self else attr[key]
        return self
    
class RGB:
    
    MIXNUM = 161
    
    @classmethod
    def __pos_mix__(cls, c):
        return (c + cls.MIXNUM) % 256 
    
    @classmethod
    def __neg_mix__(cls, c):
        return (c + 255 - cls.MIXNUM) % 256
    
    def __init__(self, r=51, g=102, b=255):
        self.r = r
        self.g = g
        self.b = b
        
    def getRGB(self):
        return self.r, self.g, self.b
    
    def getNext(self):
        r = self.r
        g = self.g
        b = self.b
        self.r = RGB.__neg_mix__(self.r)
        self.g = RGB.__neg_mix__(self.g)
        self.b = RGB.__pos_mix__(self.b)
        return r, g, b

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
        VIEW.__init__(self, 'p', **ATTR.merge(attrs, {'class' : 'para'}))

class ANCH(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'a', **attrs)

class LABEL(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'label', **attrs)

class STRONG(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'strong', **attrs)

class SMALL(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'small', **attrs)
        
class IMG(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'img', **attrs)

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
        VIEW.__init__(self, 'button', **ATTR.merge(attrs, {'class' : 'btn', 'type' : 'button'}))
