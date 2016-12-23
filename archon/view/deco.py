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

class ROW(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'row'}))

class COL(DIV):
    
    def __init__(self, size, scr='xs', **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'col-%s-%d colwrapper' % (scr, size)}))

class POL(DIV):
    
    def __init__(self, size, scr='xs', **attrs):
        DIV.__init__(self, **{'class' : 'col-%s-%d colwrapper' % (scr, size)})
        self.idiv = DIV(**ATTR.merge(attrs, {'class' : 'panelcol'}))
        self['elements'].append(self.idiv)
    
    def html(self, *elements):
        self.idiv.html(*elements)
        return self

class Icon(VIEW):
    
    def __init__(self, icon, **attrs):
        VIEW.__init__(self, 'i', **ATTR.merge(attrs, {'class' : 'fa fa-%s' % icon}))

# class KeyVal(PARA):
#     def __init__(self, key, val, **attrs):
#         PARA.__init__(self, **ATTR.merge(attrs, {'class' : 'keyval'}))
#         self.html(SPAN(**{'class' : 'keyval-key'}).html(key).html(' :&nbsp;')).html(SPAN().html(val + '&nbsp;'))

class KeyVal(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'keyval'}))
        self.table = TABLE()
        self.html(self.table)
    
    def Data(self, key, val):
        self.table.html(
            TR().html(
                TH().html(key)
            ).html(
                TD().html(val)
            )
        )

class Alert(DIV):
    
    def __init__(self, title, msg, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'alert alert-dismissible', 'role' : 'alert'}))
        self.html(
            VIEW('button', **{'type' : 'button', 'class' : 'close', 'data-dismiss' : 'alert', 'aria-label' : 'Close'}).html(
                SPAN(**{'aria-hidden' : 'true'}).html('&times;')
            )
        ).html(STRONG().html(title)).html(msg)

class Panel(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'panel'}))
        self.head = DIV(**{'class' : 'panel-heading'})
        self.body = DIV(**{'class' : 'panel-body'})
        self.foot = DIV(**{'class' : 'panel-footer'})
    
    def Head(self, element):
        self.head.html(element)
        if self.head not in self['elements']: self['elements'].insert(0, self.head)
        return self
    
    def Body(self, element):
        self.body.html(element)
        if self.body not in self['elements']: self['elements'].insert(-1, self.body)
        return self
    
    def Foot(self, element):
        self.foot.html(element)
        if self.foot not in self['elements']: self['elements'].append(self.foot)
        return self

class CountPanel(DIV):
    
    def __init__(self, title, icon, count, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'panel'}))
        self.html(
            DIV(**{'class' : 'panel-heading'}).html(
                ROW().html(
                    COL(4).html(
                        Icon(icon, **{'class' : 'fa-5x'})
                    )
                ).html(
                    COL(8, **{'class' : 'text-right'}).html(
                        DIV(**{'class' : 'huge-font'}).html(str(count))
                    ).html(
                        DIV().html(STRONG().html(title))
                    )
                )
            )
        )
    
class Indent(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **ATTR.merge(attrs, {'class' : 'indent'}))

class Section(DIV):
    
    def __init__(self, title, **attrs):
        DIV.__init__(self)
        self.body = Indent(**attrs)
        self['elements'].append(HEAD(3).html(title))
        self['elements'].append(self.body)
        
    def html(self, *elements):
        for element in elements: self.body.html(element)
        return self

class Navigation(DIV):
     
    def __init__(self, **attrs):
        DIV.__init__(self, **attrs)
        self.uuid = VIEW.getUUID()
        self.tab_cnt = 0
        self.tab_first = True
        self.tab = UL(**{'class' : 'nav nav-tabs', 'role' : 'tablist'})
        self.content = DIV(**{'class' : 'tab-content'})
        self.html(self.tab).html(self.content)
        
    def Tab(self, label, element):
        tid = '%s-%d' % (self.uuid, self.tab_cnt)
        self.tab_cnt += 1
        if self.tab_first:
            lattr = {'role' : 'presentation', 'class' : 'active'}
            dattr = {'role' : 'tabpanel', 'class' : 'tab-pane fade in active', 'id' : tid}
            self.tab_first = False
        else:
            lattr = {'role' : 'presentation'}
            dattr = {'role' : 'tabpanel', 'class' : 'tab-pane fade', 'id' : tid}
        self.tab.html(
            LI(**lattr).html(
                ANCH(**{'href' : '#%s' % tid, 'aria-controls' : tid, 'role' : 'tab', 'data-toggle' : 'tab'}).html(label)
            )
        )
        self.content.html(DIV(**dattr).html(element))

class Modal(DIV):
    
    class Close(BUTTON):
        def __init__(self, text='Close', **attrs):
            BUTTON.__init__(self, **ATTR.merge(attrs, {'data-dismiss' : 'modal'}))
            self.html(text)
    
    def __init__(self, modal_title, click_element, **attrs):
        DIV.__init__(self)
        uuid = VIEW.getUUID()
        label_id = uuid + '-label'
        click_element['attrs']['data-toggle'] = 'modal'
        click_element['attrs']['data-target'] = '#%s' % uuid
        self['elements'].append(click_element)
        self.body = DIV(**ATTR.merge(attrs, {'class' : 'modal-body'}))
        self['elements'].append(DIV(**{'class' : 'modal fade', 'id' : uuid, 'tabindex' : '-1', 'role' : 'dialog', 'aria-labelledby' : label_id}).html(
                DIV(**{'class' : 'modal-dialog', 'role' : 'document'}).html(
                    DIV(**{'class' : 'modal-content'}).html(
                        DIV(**{'class' : 'modal-header'}).html(
                            VIEW('button', **{'class' : 'close', 'data-dismiss' : 'modal', 'aria-label' : 'Close'}).html(SPAN(**{'aria-hidden' : 'true'}).html('&times;'))
                        ).html(
                            HEAD(4, **{'class' : 'modal-title', 'id' : label_id}).html(modal_title)
                        )
                    ).html(
                        self.body
                    )
                )
            )
        )

    def html(self, *elements):
        for element in elements: self.body.html(element)
        return self