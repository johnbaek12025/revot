import re
import os
import json

from django.http import HttpResponse


class CheckAllowedCookie:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'dev_cookie' in request.META:
            response = self.get_response(request)
            response.set_cookie('login', 'V2KVZTPJUOCdcuP3Q7fSVT3BYLS4dGxVfWZAPeUgaerIbEKUiMDmhJf3Ht7yMdfP3ESE', max_age=365 * 24 * 60 * 60, httponly=False, samesite='None')
            return response

        response = self.get_response(request)
        return response

            
        