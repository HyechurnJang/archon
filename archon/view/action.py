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

class Get(STRONG):
    
    def __init__(self, url, **attrs):
        STRONG.__init__(self, **ATTR.merge(attrs, {'class' : 'data-action', 'onclick' : "GetData('%s');" % url}))

class Post(DIV):
    
    class TopLabel(LABEL):
        def __init__(self, label, **attrs):
            LABEL.__init__(self, **attrs)
            self.html(label)
            
    class InLabel(SPAN):
        def __init__(self, label, **attrs):
            SPAN.__init__(self, **ATTR.merge(attrs, {'class' : 'input-group-addon'}))
            self.html(label)
     
    def __init__(self, url, label='Submit', **attrs):
        DIV.__init__(self)
        self.uuid = VIEW.getUUID()
        self.html(
            DIV(**{'class' : 'input-group'}).html(
                BUTTON(**ATTR.merge(attrs, {'onclick' : "PostData('." + self.uuid + "','%s');" % url})).html(label)
            )
        )
         
    def Text(self, name, label, **attrs):
        self['elements'].insert(-1,
            DIV(**{'class' : 'input-group'}).html(label).html(
                INPUT(**ATTR.merge(attrs, {'type' : 'text', 'name' : name, 'class' : 'form-control ' + self.uuid}))
            )
        )
        return self
    
    def Password(self, name='password', label='Password', **attrs):
        self['elements'].insert(-1,
            DIV(**{'class' : 'input-group'}).html(label).html(
                INPUT(**ATTR.merge(attrs, {'type' : 'password', 'name' : name, 'class' : 'form-control ' + self.uuid}))
            )
        )
        return self
    
class Delete(ANCH):
    
    def __init__(self, element, url, **attrs):
        ANCH.__init__(self, **ATTR.merge(attrs, {'class' : 'data-action', 'onclick' : "DeleteData('%s');" % url}))
        self.html(element)

class DelClick(VIEW):
    
    def __init__(self, url, tail=False, **attrs):
        if tail: VIEW.__init__(self, 'button', **ATTR.merge(attrs, {'class' : 'close', 'onclick' : "DeleteData('%s');" % url}))
        else: VIEW.__init__(self, 'button', **ATTR.merge(attrs, {'class' : 'close', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:none;'}))
        self.html('&times;')

class DelButton(BUTTON):
    
    def __init__(self, url, text='Delete', tail=False, **attrs):
        if tail: BUTTON.__init__(self, **ATTR.merge(attrs, {'class' : 'btn-danger', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:right;'}))
        else: BUTTON.__init__(self, **ATTR.merge(attrs, {'class' : 'btn-danger', 'onclick' : "DeleteData('%s');" % url}))
        self.html(text)
