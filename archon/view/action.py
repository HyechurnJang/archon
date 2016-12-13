'''
Created on 2016. 12. 13.

@author: Hye-Churn Jang
'''

from core import *

class Get(ANCH):
    
    def __init__(self, element, url, **attrs):
        VIEW.setAttrs({'class' : 'data-action', 'onclick' : "GetData('%s');" % url}, attrs)
        ANCH.__init__(self, **attrs)
        self.html(element)

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