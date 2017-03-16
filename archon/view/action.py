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

class GET(STRONG):
    
    def __init__(self, url, **attrs):
        STRONG.__init__(self, **TAG.ATTR(attrs, CLASS='data-action', **{'onclick':"GetData('%s');" % url}))

class POST(DIV):
    
    class LABEL_TOP(LABEL):
        def __init__(self, label, **attrs):
            LABEL.__init__(self, **attrs)
            self.html(label)
            
    class LABEL_INLINE(SPAN):
        def __init__(self, label, **attrs):
            SPAN.__init__(self, **TAG.ATTR(attrs, CLASS='input-group-addon'))
            self.html(label)
     
    def __init__(self, url, label='Submit', **attrs):
        DIV.__init__(self)
        self.uuid = TAG.UUID()
        self.html(
            DIV(CLASS='input-group').html(
                BUTTON(**TAG.ATTR(attrs, **{'onclick':"PostData('." + self.uuid + "','%s');" % url})).html(label)
            )
        )
         
    def Text(self, name, label, **attrs):
        self['elems'].insert(-1,
            DIV(CLASS='input-group').html(
                label,
                INPUT(**TAG.ATTR(attrs, TYPE='text', NAME=name, CLASS='form-control ' + self.uuid))
            )
        )
        return self
    
    def Password(self, name='password', label='Password', **attrs):
        self['elems'].insert(-1,
            DIV(CLASS='input-group').html(
                label,
                INPUT(**TAG.ATTR(attrs, TYPE='password', NAME=name, CLASS='form-control ' + self.uuid))
            )
        )
        return self
    
    def Select(self, name, label='Select', *elems, **attrs):
        select = SELECT(**TAG.ATTR(attrs, NAME=name, CLASS='form-control ' + self.uuid))
        for elem in elems: select.html(OPTION().html(elem))
        self['elems'].insert(-1,
            DIV(CLASS='input-group').html(
                label,
                select
            )
        )
        return self

class UPLOAD(FORM):
    
    def __init__(self, url, name, label='Select File', submit='Upload', **attrs):
        self.uuid = TAG.UUID()
        FORM.__init__(self, **TAG.ATTR(attrs, ID=self.uuid, CLASS='form-inline', method='post'))
        self.html(
            DIV(CLASS='input-group').html(
                SPAN(CLASS='input-group-addon', STYLE='border-color:#337ab7;').html(STRONG().html(label)),
                INPUT(ID=self.uuid + '-file', TYPE='file', NAME=name, CLASS='form-control', STYLE='border-color:#337ab7;border-right:0px;'),
                ANCH(CLASS='btn btn-primary', STYLE='display:table-cell;border-radius:0px 5px 5px 0px;', href="javascript:PostFile('%s','%s');" % (self.uuid, url)).html(
                    ICON('arrow-circle-up'), ' ', submit
                )
            )
        )
    
class DELETE(ANCH):

    class CLICK(TAG):
    
        def __init__(self, url, tail=False, **attrs):
            if tail: TAG.__init__(self, 'button', **TAG.ATTR(attrs, CLASS='close', **{'onclick':"DeleteData('%s');" % url}))
            else: TAG.__init__(self, 'button', **TAG.ATTR(attrs, CLASS='close', STYLE='float:none;', **{'onclick':"DeleteData('%s');" % url}))
            self.html('&times;')
    
    class BUTTON(BUTTON):
        
        def __init__(self, url, text='Delete', tail=False, **attrs):
            if tail: BUTTON.__init__(self, **TAG.ATTR(attrs, CLASS='btn-danger', STYLE='float:right;', **{'onclick' : "DeleteData('%s');" % url}))
            else: BUTTON.__init__(self, **TAG.ATTR(attrs, CLASS='btn-danger', **{'onclick' : "DeleteData('%s');" % url}))
            self.html(text)
    
    def __init__(self, elem, url, **attrs):
        ANCH.__init__(self, **TAG.ATTR(attrs, CLASS='data-action', **{'onclick':"DeleteData('%s');" % url}))
        self.html(elem)
