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
    def __init__(self, **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='row'))

class COL(DIV):
    def __init__(self, size, scr='sm', **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='col-%s-%d colwrapper' % (scr, size)))

class STRWRAP(DIV):
    def __init__(self, width=100, **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='strwrap', STYLE='width:%dpx;' % width))

class KEYVAL(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **TAG.ATTR(attrs, CLASS='keyval'))
        self.table = TABLE()
        self.html(self.table)
        self.first = False
    
    def Data(self, key, val):
        if self.first: self.table.html(TR().html(TH().html(key)).html(TD().html(val)))
        else:
            self.table.html(TR().html(TH(CLASS='keyval-first').html(key)).html(TD(CLASS='keyval-first').html(val)))
            self.first = True
        return self
    
    def __len__(self, *args, **kwargs):
        return self.table.__len__()

class ALERT(DIV):
    
    def __init__(self, title, msg, **attrs):
        DIV.__init__(self, **TAG.ATTR(attrs, CLASS='alert alert-dismissible', **{'role':'alert'}))
        self.html(
            TAG('button', TYPE='button', CLASS='close', **{'data-dismiss':'alert', 'aria-label':'Close'}).html(
                SPAN(**{'aria-hidden':'true'}).html('&times;')
            ),
            STRONG().html(title),
            msg
        )

class PANEL(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **TAG.ATTR(attrs, CLASS='panel'))
        self.head = DIV(CLASS='panel-heading')
        self.body = DIV(CLASS='panel-body')
        self.foot = DIV(CLASS='panel-footer')
    
    def Head(self, *elems):
        self.head.html(*elems)
        if self.head not in self['elems']: self['elems'].insert(0, self.head)
        return self
    
    def Body(self, *elems):
        self.body.html(*elems)
        if self.body not in self['elems']: self['elems'].append(self.body)
        return self
    
    def Foot(self, *elems):
        self.foot.html(*elems)
        if self.foot not in self['elems']: self['elems'].append(self.foot)
        return self

class COUNTER(DIV):
    
    def __init__(self, title, icon, count, **attrs):
        DIV.__init__(self, **TAG.ATTR(attrs, CLASS='panel'))
        self.html(
            DIV(CLASS='panel-heading').html(
                ROW().html(
                    COL(4).html(ICON(icon, CLASS='fa-5x')),
                    COL(8, CLASS='text-right').html(
                        DIV(CLASS='huge-font').html(str(count)),
                        DIV().html(STRONG().html(title))
                    )
                )
            )
        )
    
class INDENT(DIV):
    
    def __init__(self, **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='indent'))

class SECTOR(DIV):
    
    def __init__(self, title, **attrs):
        DIV.__init__(self)
        self.body = INDENT(**attrs)
        self['elems'].append(HEAD(3).html(title))
        self['elems'].append(self.body)
        
    def html(self, *elems):
        self.body.html(*elems)
        return self

class LISTGROUP(UL):
    
    def __init__(self, **attrs):
        UL.__init__(self, **TAG.ATTR(attrs, CLASS='list-group'))
    
    def html(self, *elems):
        for elem in elems: self['elems'].append(LI(CLASS='list-group-item').html(elem))
        return self

class NAV(DIV):
     
    def __init__(self, **attrs):
        DIV.__init__(self, **attrs)
        self.uuid = TAG.UUID()
        self.tab_cnt = 0
        self.tab_first = True
        self.tab = UL(CLASS='nav nav-tabs', **{'role':'tablist'})
        self.content = DIV(CLASS='tab-content')
        self.html(self.tab).html(self.content)
        
    def Tab(self, label, elem):
        tid = '%s-%d' % (self.uuid, self.tab_cnt)
        self.tab_cnt += 1
        if self.tab_first:
            lattr = {'CLASS':'active', 'role':'presentation'}
            dattr = {'ID':tid, 'CLASS':'tab-pane fade in active', 'role':'tabpanel'}
            self.tab_first = False
        else:
            lattr = {'role':'presentation'}
            dattr = {'ID':tid, 'CLASS':'tab-pane fade', 'role':'tabpanel'}
        self.tab.html(
            LI(**lattr).html(
                ANCH(**{'href':'#%s' % tid, 'aria-controls':tid, 'role':'tab', 'data-toggle':'tab'}).html(label)
            )
        )
        self.content.html(DIV(**dattr).html(elem))
        return self

class MODAL(DIV):
    
    class CLOSE(BUTTON):
        def __init__(self, text='Close', **attrs):
            BUTTON.__init__(self, **TAG.ATTR(attrs, **{'data-dismiss':'modal'}))
            self.html(text)
    
    def __init__(self, modal_title, click_element, **attrs):
        DIV.__init__(self)
        uuid = TAG.UUID()
        label_id = uuid + '-label'
        click_element['attrs']['data-toggle'] = 'modal'
        click_element['attrs']['data-target'] = '#%s' % uuid
        self['elems'].append(click_element)
        self.body = DIV(**TAG.ATTR(attrs, CLASS='modal-body'))
        self['elems'].append(
            DIV(CLASS='modal fade', ID=uuid, **{'tabindex':'-1', 'role':'dialog', 'aria-labelledby':label_id}).html(
                DIV(CLASS='modal-dialog', **{'role':'document'}).html(
                    DIV(CLASS='modal-content').html(
                        DIV(CLASS='modal-header').html(
                            TAG('button', CLASS='close', **{'data-dismiss':'modal', 'aria-label':'Close'}).html(
                                SPAN(**{'aria-hidden':'true'}).html('&times;')
                            ),
                            HEAD(4, CLASS='modal-title', ID=label_id).html(modal_title)
                        ),
                        self.body
                    )
                )
            )
        )

    def html(self, *elems):
        self.body.html(*elems)
        return self

class JUMBO(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **TAG.ATTR(attrs, CLASS='jumbotron'))

class FLIPCLOCK(TAG):
    
    def __init__(self, **attrs):
        TAG.__init__(self, 'DIV', **TAG.ATTR(attrs, ID=TAG.UUID(), LIB='flipclock'))

class OVERLAP(DIV):
    
    def __init__(self, width, height=None, **attrs):
        style = 'width:%dpx;' % width
        if height != None: style += 'height:%dpx;' %  height
        DIV.__init__(self, **TAG.ATTR(attrs, STYLE=style))
        self.over = DIV(STYLE='position:absolute;' + style)
        self.under = DIV(STYLE=style)
        self.html(self.over, self.under)
    
    def Under(self, *elems):
        self.under.html(*elems)
        return self
    
    def Over(self, *elems):
        self.over.html(*elems)
        return self
    
    