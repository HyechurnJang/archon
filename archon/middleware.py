'''
Created on 2016. 11. 3.

@author: Hye-Churn Jang
'''

class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)