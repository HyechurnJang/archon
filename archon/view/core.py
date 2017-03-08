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

import re
import uuid

class TAG(dict):
    
    @classmethod
    def ATTR(cls, attrs, **sets):
        for k in sets: attrs[k] = '%s %s' % (sets[k], attrs[k]) if k in attrs else sets[k]
        return attrs
    
    @classmethod
    def UUID(cls):
        return 'V-' + str(uuid.uuid4())
    
    def __init__(self, tag, **attrs):
        dict.__init__(self, tag=tag, elems=[], attrs=attrs)
    
    def __len__(self, *args, **kwargs):
        return self['elems'].__len__()
    
    def __str__(self):
        return self.render()
    
    def click(self, url):
        if 'CLASS' in self['attrs']: self['attrs']['CLASS'] += ' clickable'
        else: self['attrs']['CLASS'] = 'clickable'
        self['attrs']['onclick'] = "GetData('%s');" % url
        return self
    
    def html(self, *elems):
        for elem in elems: self['elems'].append(elem)
        return self
    
    def empty(self):
        return not self['elems'].__len__()
    
    def render(self):
        tag = self['tag']
        attrs = self['attrs']
        elems = self['elems']
        
        attr_str = ''; 
        for k in attrs: attr_str += ' %s="%s"' % (k, attrs[k])
        
        elem_str = ''
        for elem in elems: elem_str += str(elem)
        
        return '<%s%s>%s</%s>' % (tag, attr_str, elem_str, tag)

class DIV(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'div', **attrs)

class SPAN(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'span', **attrs)

class HEAD(TAG):
    def __init__(self, level, **attrs): TAG.__init__(self, 'h' + str(level), **attrs)

class PARA(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'p', **TAG.ATTR(attrs, CLASS='para'))

class ANCH(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'a', **attrs)

class LABEL(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'label', **attrs)

class STRONG(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'strong', **attrs)

class SMALL(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'small', **attrs)
        
class IMG(TAG):
    def __init__(self, src, **attrs): TAG.__init__(self, 'img', **TAG.ATTR(attrs, src=src))
    
class ICON(TAG):
    def __init__(self, icon, **attrs): TAG.__init__(self, 'i', **TAG.ATTR(attrs, CLASS='fa fa-%s' % icon))

class THEAD(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'thead', **attrs)
        
class TBODY(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'tbody', **attrs)
        
class TH(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'th', **attrs)
        
class TR(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'tr', **attrs)

class TD(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'td', **attrs)

class TABLE(TAG):
    
    class BASIC(TAG):
        
        def __init__(self, *heads, **options):
            TAG.__init__(self, 'TABLE', ID=TAG.UUID(), CLASS='table table-bordered table-hover', LIB='table_basic', **{'width':'100%'})
            self.body = TBODY()
            self['options'] = options
            tr = TR()
            order = [None for i in range(0, len(heads))]
            for i in range(0, len(heads)):
                head = heads[i]
                kv = re.match('.+\<(?P<p>\d+)(?P<d>(\+|\-))\>$', head)
                if kv:
                    p = int(kv.group('p'))
                    d = kv.group('d')
                    if d == '+': order[p] = [i, 'asc']
                    else: order[p] = [i, 'desc']
                    head = head.replace('<%d%s>' % (p, d), '')
                tr.html(TH().html(head))
            order = filter(None, order)
            if order: self['options']['order'] = order
            else: self['options']['order'] = [[0, 'asc']]
            self.html(THEAD().html(tr)).html(self.body)
            
        def Record(self, *cols, **attrs):
            tr = TR(**attrs)
            for col in cols: tr.html(TD().html(col))
            self.body.html(tr)
            return self
        
        def __len__(self, *args, **kwargs):
            return self.body.__len__()
    
    class ASYNC(TAG):
        
        @classmethod
        def pageview(cls):
            
            def wrapper(view):
        
                def decofunc(r, m, v):
                    r.Draw = int(r.Query['draw'])
                    if isinstance(r.Draw, list): r.Draw = r.Draw[0]
                    r.Length = int(r.Query['length'])
                    if isinstance(r.Length, list): r.Length = r.Length[0]
                    r.Start = int(r.Query['start'])
                    if isinstance(r.Start, list): r.Start = r.Start[0]
                    
                    try:
                        r.OrderCol = int(r.Query['order[0][column]'])
                        if isinstance(r.OrderCol, list): r.OrderCol = r.OrderCol[0]
                        r.OrderDir = r.Query['order[0][dir]']
                        if isinstance(r.OrderDir, list): r.OrderDir = r.OrderDir[0]
                        r.Search = r.Query['search[value]']
                        if isinstance(r.Search, list): r.Search = r.Search[0]
                        if r.Search == '': r.Search = None
                    except: pass
                    
                    r.Page = r.Start / r.Length
                    
                    return view(r, m, v)
                
                return decofunc
            
            return wrapper
        
        def __init__(self, url, *heads, **attrs):
            TAG.__init__(self, 'TABLE', **TAG.ATTR(attrs, ID=TAG.UUID(), CLASS='table table-bordered table-hover', LIB='table_async', **{'width':'100%', 'url':url}))
            tr = TR()
            for head in heads: tr.html(TH().html(head))
            self.html(THEAD().html(tr))
    
    class ASYNCDATA(dict):
        
        def __init__(self, draw, total, count):
            dict.__init__(self, draw=draw, recordsTotal=total, recordsFiltered=count)
            self.data = []
            self['data'] = self.data
        
        def Record(self, *cols, **attrs):
            self.data.append([str(col) for col in cols])
            return self
        
    class FLIP(TAG):
        
        def __init__(self, *heads, **attrs):
            TAG.__init__(self, 'TABLE', **TAG.ATTR(attrs, ID=TAG.UUID(), CLASS='table', LIB='table_flip', **{'data-show-toggle':'true', 'data-paging':'true', 'width':'100%'}))
            self.body = TBODY()
            tr = TR()
            for head in heads:
                if '+' in head: tr.html(TH(**{'data-type':'html', 'data-breakpoints':'all', 'data-title':head.replace('+', '')}).html(head))
                else: tr.html(TH(**{'data-type':'html'}).html(head))
            self.html(THEAD().html(tr)).html(self.body)
            
        def Record(self, *cols, **attrs):
            tr = TR(**attrs)
            for col in cols: tr.html(TD(**{'data-type':'html'}).html(col))
            self.body.html(tr)
            return self
        
        def __len__(self, *args, **kwargs):
            return self.body.__len__()
    
    def __init__(self, **attrs): TAG.__init__(self, 'table', **attrs)
        
class UL(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'ul', **attrs)

class LI(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'li', **attrs)

class FORM(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'form', **attrs)

class INPUT(TAG):
        def __init__(self, **attrs): TAG.__init__(self, 'input', **attrs)

class SELECT(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'select', **attrs)

class OPTION(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'option', **attrs)

class BUTTON(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'button', **TAG.ATTR(attrs, CLASS='btn', TYPE='button'))
