'''
Created on 2017. 1. 4.

@author: Hye-Churn Jang
'''

import re
import json
from BeautifulSoup import BeautifulSoup

if __name__ == '__main__':
    
    with open('apic_faults.html', 'r') as fd: html = fd.read()
    bs = BeautifulSoup(html)
    
    sections = bs.findAll('section')
    
    fixtures = []
    
    for s in sections:
        raw_head = s.contents[1].contents[3]
        head = re.match('(?P<code>\w+)\s+-\s+(?P<title>\w+)\s*', raw_head)
        code = head.group('code')
        title = head.group('title')
        syslog = re.sub('\s+', ' ', s.contents[5].contents[-1])
        explan = re.sub('\s+', ' ', s.contents[9].contents[-1])
        
        actions = []
        first_step = s.findAll('p', **{'class' : 'pSF_StepFirst'})
        if first_step:
            actions.append(re.sub('\s+', ' ', first_step[0].contents[-1][1:]))
        next_step = s.findAll('p', **{'class' : 'pSN_StepNext'})
        for n in next_step:
            actions.append(re.sub('\s+', ' ', n.contents[-1][1:]))
        if not actions:
            actions.append(re.sub('\s+', ' ', s.contents[-2].contents[-1]))
        actions = '\n'.join(actions)
        
        data = {'model' : 'aci.FaultMessage', 'fields' : {'code' : code, 'title' : title, 'syslog' : syslog, 'explan' : explan, 'actions' : actions}}
        fixtures.append(data)
    
    fixtures = json.dumps(fixtures, indent=2)
    with open('apic_faults.json', 'w') as fd: fd.write(fixtures)
