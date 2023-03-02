from django.urls import reverse
import json
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from main.commonutility import BaseJsonFormat, get_client_ip
from main.models.client import ClientIp, User
from django.contrib.auth.hashers import check_password
from main.models.security import LoginSession
from main.views.security import ParsedClientView, generate_login_cookie
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


class LogIn(View):    
    def get(self, req, **kwargs):       
        print(kwargs)
        context = dict()
        context.update(kwargs)        
        return render(req, 'login.html', context=context)
    
    
    def post(self, req):
        data = req.POST
        res = HttpResponseRedirect(reverse('main:login'))
        print(data)
        account = data['user']
        password = data['pwd']
        remember_account = data.get('remember_account', None)                 
        try:
            client = User.objects.get(email_account=account)           
        except User.DoesNotExist:
            err_msg = "계정 정보가 존재하지 않습니다."            
            res = HttpResponseRedirect(reverse('main:login'))
            messages.error(req, err_msg)
            return res
        if not client:
            err_msg = "계정 정보가 존재하지 않습니다."
            res = HttpResponseRedirect(reverse('main:login'))
            messages.error(req, err_msg)
            return res
            
        hash_pwd = client.password
        if check_password(password, hash_pwd):            
            if client.authorization:
                try:
                    client_ip = ClientIp.objects.get(ip_address=get_client_ip(req))
                except ClientIp.DoesNotExist:
                    client_ip = ClientIp(ip_address=get_client_ip(req))
                    client_ip.save()
                login_cookie_value = generate_login_cookie(
                    account=client, user_agent=req.META['HTTP_USER_AGENT'], ip=client_ip
                )
                if not remember_account:
                    req.session.set_expiry(0)
                if not remember_account:
                    req.session.set_expiry(1209600)
                res = HttpResponseRedirect(reverse('main:main'))
                res.set_cookie('login', login_cookie_value, max_age=60 * 60 * 24 * 6, httponly=True)                
                return res
            else:                
                err_msg = "승인 대기 중인 계정입니다. 관리자 승인 이후 정상 로그인됩니다."                
                res = HttpResponseRedirect(reverse('main:login'))
                messages.error(req, err_msg)
                return res
        else:
            err_msg = "계정 정보가 존재하지 않습니다."            
            res = HttpResponseRedirect(reverse('main:login'))
            messages.error(req, err_msg)
            return res


class LogOut(View):
    @transaction.atomic
    def get(self, req):        
        res = HttpResponseRedirect(reverse('main:login'))
        cookie_value = req.COOKIES.get('login', None)
        if cookie_value:
            login_session = LoginSession.objects.get(value=cookie_value)
            login_session.logged_out = True
            login_session.save()            
            res.delete_cookie('login')        
        return res
    