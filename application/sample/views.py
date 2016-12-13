import archon

from archon import pageview
from archon.view import *

# Create your views here.

class SampleManager(archon.Manager): pass

@pageview(SampleManager)
def information(manager, request, method, path, query, data, menu):
    return '''<h1>Hello Blank</h1>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            <br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>HELLO<br/>
            Hello Finished'''

@pageview(SampleManager)
def document(manager, request, method, path, query, data, menu):
    return 'Document'

@pageview(SampleManager)
def jsondata(manager, request, method, path, query, data, menu):
    return DIV().add(DIV().add(DIV().add(DIV().add('Json'))))

