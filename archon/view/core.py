'''
Created on 2016. 11. 30.

@author: Hye-Churn Jang
'''

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
    
    def isEmpty(self):
        if len(self['elements']) == 0: return True
        return False

class DIV(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'div', **attrs)

class SPAN(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'span', **attrs)

class HEADER(VIEW):
    def __init__(self, level, **attrs):
        VIEW.__init__(self, 'h' + str(level), **attrs)

class PARA(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'p', **attrs)

class LABEL(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'label', **attrs)

class ANC(VIEW):
    def __init__(self, **attrs):
        VIEW.__init__(self, 'a', **attrs)
        
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
