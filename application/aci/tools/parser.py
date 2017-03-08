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
