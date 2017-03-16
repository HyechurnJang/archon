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

"""
WSGI config for archon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import sys
from openpyxl import load_workbook
from django.core.wsgi import get_wsgi_application
from .settings import INSTALLED_APPS
from .manager import Manager

def getLocaleFromXLSX(path):
    wb = load_workbook(filename=path)
    sheet = wb['locale']
    sheet_langs = sheet['1']
    sheet_keys = sheet['A']
    langs = []
    keys = []
    locale = {}
    
    for sheet_lang in sheet_langs[1:]: langs.append(sheet_lang.value)
    for sheet_key in sheet_keys[1:]: keys.append(sheet_key.value)
    for i in range(0, len(keys)):
        vals = sheet[str(i + 2)]
        key = keys[i]
        locale[key] = {}
        
        for j in range(0, len(vals) - 1):
            val = vals[j + 1].value
            if val != None: locale[key][langs[j]] = val
    
    return locale

print('\n2. Loading locales')
sys.stdout.write('%-40s =====> ' % './archon/locale.xlsx')
archon_locales = {'GLOBAL' : getLocaleFromXLSX('./archon/locale.xlsx')}
print('[ OK ]')
for app in INSTALLED_APPS:
    if 'application.' in app:
        app_name = app.split('.')[-1]
        locale_path = './' + app.replace('.', '/') + '/locale.xlsx'
        sys.stdout.write('%-40s =====> ' % locale_path)
        archon_locales[app_name] = getLocaleFromXLSX(locale_path)
        print('[ OK ]')
__builtins__['archon_locales'] = archon_locales

print('\n3. Loading archon manager')
sys.stdout.write('%-40s =====> ' % 'Archon Manager')
__builtins__['Archon'] = Manager.instance()
print('[ OK ]')

print('\n4. Loading application managers')
for app in INSTALLED_APPS:
    if 'application.' in app:
        manager_path = app + '.manager'
        fromlist = app.split('.')
        sys.stdout.write('%-40s =====> ' % manager_path)
        __import__(manager_path, globals(), fromlist=fromlist).Manager.instance()
        print('[ OK ]')

print('\n5. Archon Initialization Finished >> Logging Start')
application = get_wsgi_application()