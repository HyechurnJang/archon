'''
Created on 2016. 12. 13.

@author: Hye-Churn Jang
'''

from core import *

class ROW(DIV):
    def __init__(self, **attrs):
        VIEW.setAttrs({'class' : 'row'}, attrs)
        DIV.__init__(self, **attrs)

class COL(DIV):
    def __init__(self, size, scr='md', **attrs):
        VIEW.setAttrs({'class' : 'col-%s-%d' % (scr, size)}, attrs)
        DIV.__init__(self, **attrs)

class Icon(VIEW):
    
    def __init__(self, icon, **attrs):
        VIEW.setAttrs({'class' : 'fa fa-%s' % icon}, attrs)
        VIEW.__init__(self, 'i', **attrs)

class KeyVal(PARA):
    
    def __init__(self, key, val, **attrs):
        VIEW.setAttrs({'class' : 'keyval'}, attrs)
        PARA.__init__(self, **attrs)
        self.html(SPAN(**{'class' : 'keyval-key'}).html(key).html(' :&nbsp;')).html(SPAN().html(val + '&nbsp;'))

class Alert(DIV):
    
    def __init__(self, title, msg, **attrs):
        VIEW.setAttrs({'class' : 'alert alert-dismissible', 'role' : 'alert'}, attrs)
        DIV.__init__(self, **attrs)
        self.html(
            VIEW('button', **{'type' : 'button', 'class' : 'close', 'data-dismiss' : 'alert', 'aria-label' : 'Close'}).html(
                SPAN(**{'aria-hidden' : 'true'}).html('&times;')
            )
        ).html(
            VIEW('strong').html(title)
        ).html(
            msg
        )

class Modal(DIV):
    
    class Close(BUTTON):
        def __init__(self, text='Close', **attrs):
            VIEW.setAttrs({'data-dismiss' : 'modal'}, attrs)
            BUTTON.__init__(self, **attrs)
            self.html(text)
    
    def __init__(self, modal_title, click_element, **attrs):
        DIV.__init__(self)
        uuid = VIEW.getUUID()
        label_id = uuid + '-label'
        
        click_element['attrs']['data-toggle'] = 'modal'
        click_element['attrs']['data-target'] = '#%s' % uuid
        self['elements'].append(click_element)
        
        VIEW.setAttrs({'class' : 'modal-body'}, attrs)
        self.body = DIV(**attrs)
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

    def html(self, element):
        self.body.html(element)
        return self
    
class Panel(DIV):
    
    def __init__(self, **attrs):
        VIEW.setAttrs({'class' : 'panel'}, attrs)
        DIV.__init__(self, **attrs)
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
