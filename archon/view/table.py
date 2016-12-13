'''
Created on 2016. 12. 13.

@author: Hye-Churn Jang
'''

from core import *

class DataTable(VIEW):
    
    def __init__(self, *heads, **attrs):
        VIEW.setAttrs({'id' : VIEW.getUUID(), 'class' : 'table table-bordered table-hover', 'width' : '100%', 'lib' : 'datatable'}, attrs)
        VIEW.__init__(self, 'TABLE', **attrs)
        self.body = TBODY()
        tr = TR()
        for head in heads: tr.html(TH().html(head))
        self.html(THEAD().html(tr)).html(self.body)
        
    def record(self, *cols, **attrs):
        tr = TR(**attrs)
        for col in cols: tr.html(TD().html(col))
        self.body.html(tr)
        return self
    
    def __len__(self, *args, **kwargs):
        return self.body.__len__()

class FooTable(VIEW):
    
    def __init__(self, *heads, **attrs):
        VIEW.setAttrs({'id' : VIEW.getUUID(), 'class' : 'table', 'data-show-toggle' : 'true', 'data-paging' : 'true', 'width' : '100%', 'lib' : 'footable'}, attrs)
        VIEW.__init__(self, 'TABLE', **attrs)
        self.body = TBODY()
        tr = TR()
        for head in heads:
            if '+' in head: tr.html(TH(**{'data-type' : 'html', 'data-breakpoints' : 'all', 'data-title' : head.replace('+', '')}).html(head))
            else: tr.html(TH(**{'data-type' : 'html'}).html(head))
        self.html(THEAD().html(tr)).html(self.body)
        
    def record(self, *cols, **attrs):
        tr = TR(**attrs)
        for col in cols: tr.html(TD().html(col))
        self.body.html(tr)
        return self
    
    def __len__(self, *args, **kwargs):
        return self.body.__len__()
