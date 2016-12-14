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

class Get(ANCH):
    
    def __init__(self, element, url, **attrs):
        VIEW.setAttrs({'class' : 'data-action', 'onclick' : "GetData('%s');" % url}, attrs)
        ANCH.__init__(self, **attrs)
        self.html(element)
        
def GetOnClick(url):
    return "GetData('%s');" % url 

class Post(DIV):
    
    class TopLabel(LABEL):
        def __init__(self, label, **attrs):
            LABEL.__init__(self, **attrs)
            self.html(label)
            
    class InLabel(SPAN):
        def __init__(self, label, **attrs):
            VIEW.setAttrs({'class' : 'input-group-addon'}, attrs)
            SPAN.__init__(self, **attrs)
            self.html(label)
     
    def __init__(self, url, label='Submit', **attrs):
        DIV.__init__(self)
        self.uuid = VIEW.getUUID()
        VIEW.setAttrs({'onclick' : "PostData('." + self.uuid + "','%s');" % url}, attrs)
        self.submit = DIV(**{'class' : 'input-group'}).html(BUTTON(**attrs).html(label))
        self.html(self.submit)
         
    def Text(self, name, label, **attrs):
        VIEW.setAttrs({'type' : 'text', 'name' : name, 'class' : 'form-control ' + self.uuid}, attrs)
        div = DIV(**{'class' : 'input-group'}).html(label).html(INPUT(**attrs))
        self['elements'].insert(-1, div)
        return self
    
    def Password(self, name='passwd', label='Password', **attrs):
        VIEW.setAttrs({'type' : 'password', 'name' : name, 'class' : 'form-control ' + self.uuid}, attrs)
        div = DIV(**{'class' : 'input-group'}).html(label).html(INPUT(**attrs))
        self['elements'].insert(-1, div)
        return self
    
class Delete(ANCH):
    
    def __init__(self, element, url, **attrs):
        VIEW.setAttrs({'class' : 'data-action', 'onclick' : "DeleteData('%s');" % url}, attrs)
        ANCH.__init__(self, **attrs)
        self.html(element)

class DelClick(VIEW):
    
    def __init__(self, url, tail=False, **attrs):
        if tail: VIEW.setAttrs({'class' : 'close', 'onclick' : "DeleteData('%s');" % url}, attrs)
        else: VIEW.setAttrs({'class' : 'close', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:none;'}, attrs)
        VIEW.__init__(self, 'button', **attrs)
        self.html('&times;')

class DelButton(BUTTON):
    
    def __init__(self, url, text='Delete', tail=False, **attrs):
        if tail: VIEW.setAttrs({'class' : 'btn-danger btn-xs', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:right;'}, attrs)
        else: VIEW.setAttrs({'class' : 'btn-danger btn-xs', 'onclick' : "DeleteData('%s');" % url}, attrs)
        BUTTON.__init__(self, **attrs)
        self.html(text)