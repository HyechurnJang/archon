'''
Created on 2016. 12. 6.

@author: Hye-Churn Jang
'''

from core import *

class Row(DIV):
    
    def __init__(self, **attrs):
        VIEW.setAttrs({'class' : 'row'}, attrs)
        DIV.__init__(self, **attrs)

class Col(DIV):
    
    def __init__(self, size, scr='md', **attrs):
        VIEW.setAttrs({'class' : 'col-%s-%d' % (scr, size)}, attrs)
        DIV.__init__(self, **attrs)

class Menu(DIV):
    
    def __init__(self, **attrs):
        DIV.__init__(self, **attrs)
    
    def html(self, element):
        if isinstance(element, VIEW):
            element['attrs']['style'] = element['attrs']['style'] + ' ' + 'float:right;padding-left:5px;' if 'style' in element['attrs'] else 'float:right;padding-left:5px;'
            DIV.html(self, element)
        else:
            DIV.html(self, SPAN(**{'style' : 'float:right;padding-left:5px;'}).html(element))
        return self
    
class KeyVal(PARA):
    
    def __init__(self, key, val, **attrs):
        VIEW.setAttrs({'style' : 'margin:0px;'}, attrs)
        PARA.__init__(self, **attrs)
        self.html(SPAN(**{'style' : 'float:left;font-weight:bold;font-size:14px;padding:0px;margin:0px;'}).html(key).html(' :&nbsp;')).html(SPAN().html(val + '&nbsp;'))

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
    
    def isEmpty(self):
        return self.body.isEmpty()

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
    
    def isEmpty(self):
        return self.body.isEmpty()
    
class Modal(DIV):
    
    class Close(BUTTON):
        def __init__(self, title='Close', **attrs):
            VIEW.setAttrs({'data-dismiss' : 'modal'}, attrs)
            BUTTON.__init__(self, **attrs)
            self.html(title)
    
    def __init__(self, click_class, click_title, modal_title, **attrs):
        DIV.__init__(self)
        uuid = VIEW.getUUID()
        label_id = uuid + '-label'
        self.element = DIV(**{'class' : 'modal-body'})
        VIEW.setAttrs({'data-toggle' : 'modal', 'data-target' : '#%s' % uuid}, attrs)
        self['elements'].append(click_class(**attrs).html(click_title))
        self['elements'].append(DIV(**{'class' : 'modal fade', 'id' : uuid, 'tabindex' : '-1', 'role' : 'dialog', 'aria-labelledby' : label_id}).html(
                DIV(**{'class' : 'modal-dialog', 'role' : 'document'}).html(
                    DIV(**{'class' : 'modal-content'}).html(
                        DIV(**{'class' : 'modal-header'}).html(
                            VIEW('button', **{'class' : 'close', 'data-dismiss' : 'modal', 'aria-label' : 'Close'}).html(SPAN(**{'aria-hidden' : 'true'}).html('&times;'))
                        ).html(
                            HEADER(4, **{'class' : 'modal-title', 'id' : label_id}).html(modal_title)
                        )
                    ).html(
                        self.element
                    )
                )
            )
        )

    def html(self, element):
        self.element.html(element)
        return self
    
class Alert(DIV):
    
    def __init__(self, title, msg, **attrs):
        VIEW.setAttrs({'class' : 'alert alert-dismissible', 'role' : 'alert'}, attrs)
        DIV.__init__(self, **attrs)
        self.html(
            VIEW('button', **{'type' : 'button', 'class' : 'close', 'data-dismiss' : 'alert', 'aria-label' : 'Close'}).html(
                SPAN(**{'aria-hidden' : 'true'}).html('&times;')
            )
        ).html(
            VIEW('strong', **{'style' : 'padding-right:10px;'}).html(title)
        ).html(
            msg
        )
        
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

class Icon(VIEW):
    
    def __init__(self, icon, **attrs):
        VIEW.setAttrs({'class' : 'fa fa-%s' % icon}, attrs)
        VIEW.__init__(self, 'i', **attrs)

class Get(ANC):
    
    def __init__(self, element, url, **attrs):
        VIEW.setAttrs({'class' : 'getdata', 'onclick' : "GetData('%s');" % url}, attrs)
        ANC.__init__(self, **attrs)
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

class DelClick(VIEW):
    def __init__(self, url, tail=False, **attrs):
        if tail: VIEW.setAttrs({'class' : 'close', 'onclick' : "DeleteData('%s');" % url}, attrs)
        else: VIEW.setAttrs({'class' : 'close', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:none;'}, attrs)
        VIEW.__init__(self, 'button', **attrs)
        self.html('&times;')

class DelButton(BUTTON):
    def __init__(self, url, label='Delete', tail=False, **attrs):
        if tail: VIEW.setAttrs({'class' : 'btn-danger btn-xs', 'onclick' : "DeleteData('%s');" % url, 'style' : 'float:right;'}, attrs)
        else: VIEW.setAttrs({'class' : 'btn-danger btn-xs', 'onclick' : "DeleteData('%s');" % url}, attrs)
        BUTTON.__init__(self, **attrs)
        self.html(label)
