from audioop import reverse
import json
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from main.commonutility import BaseJsonFormat, get_client_ip
from main.models.client import ClientIp, User
from django.contrib.auth.hashers import check_password
from main.models.security import LoginSession
from main.views.security import generate_login_cookie


class LogIn(View):
    def get(self, req, **kwargs):        
        context = dict()
        context.update(kwargs)        
        res = BaseJsonFormat(is_success=True, data=None)        
        return HttpResponse(res, content_type="application/json", status=200)
    
    def post(self, req):
        data = json.loads(req.body)
        print(data)
        account = data['user']
        password = data['pwd']
        remember_account = data['remember_account']
        print(remember_account)
        print(account)
        print(password)
        try:
            client = User.objects.get(email_account=account)            
        except User.DoesNotExist:
            err_msg = "계정 정보가 존재하지 않습니다."
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)        
        if client is None:
            err_msg = "계정 정보가 존재하지 않습니다."
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)
            
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
                res = BaseJsonFormat(data=client._user_data)
                res = HttpResponse(res, content_type="application/json")
                res.set_cookie('login', login_cookie_value, max_age=60 * 60 * 24 * 6, httponly=True)
                return res
            else:
                err_msg = "승인 대기 중인 계정입니다. 관리자 승인 이후 정상 로그인됩니다."
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)
        else:            
            err_msg = "계정 정보가 존재하지 않습니다."
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)


class LogOut(View):
    @transaction.atomic
    def get(self, req):
        res = BaseJsonFormat()
        res = HttpResponse(res, content_type="application/json", status=200)
        cookie_value = req.COOKIES.get('login', None)
        if cookie_value:
            login_session = LoginSession.objects.get(value=cookie_value)
            login_session.logged_out = True
            login_session.save()            
            res.delete_cookie('login')        
        return res
    