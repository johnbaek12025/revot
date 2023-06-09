import random
import string
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse
from django.views import View
import json
from django.http import HttpResponse, HttpResponseRedirect
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.hashers import make_password
from dummy_data import check_state_from
from main.commonutility import BaseJsonFormat, get_client_ip
from main.models.client import ClientIp, User, State
from main.views.security import generate_login_cookie
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


class JoinPage(View):
    def get(self, req, **kwargs):
        context = dict()
        context.update(kwargs)        
        # return HttpResponse(res, content_type="application/json", status=200)
        return render(req, 'join.html', context=context)
        # res = BaseJsonFormat(is_success=True, data=None)
        # return HttpResponse(res, content_type="application/json", status=200)
    
    @csrf_exempt
    @transaction.atomic
    def post(self, req):
        data = req.POST
        print(data)
        account = data['account']
        name = data['name']
        phone = data['phone']
        agency_code = data.get('agency_code', None)
        recommendation_code = data['recommendation_code']
        pwd1 = data['password1']
        pwd2 = data['password2']        
        try:            
            v = validate_email(account)
            account = v['email']
        except EmailNotValidError as e:
            err_msg = "이메일 형식이 아닙니다. 다시 작성해주세요."
            res = HttpResponseRedirect(reverse('main:join'))
            messages.error(req, err_msg)
            return res
        
        if not phone.startswith('010'):
            error_msg = '휴대전화 번호는 010 번호만 가능합니다.'
            res = HttpResponseRedirect(reverse('main:join'))
            messages.error(req, err_msg)
            return res
        
        try:
            User.objects.get(phone=phone)
        except User.DoesNotExist:
            pass
        else:            
            err_msg = '이미 해당 휴대전화로 가입된 계정이 있습니다.'
            res = HttpResponseRedirect(reverse('main:join'))
            messages.error(req, err_msg)
            return res
        
        try:
            User.objects.get(email_account=account)
        except User.DoesNotExist:
            pass
        else:
            err_msg = "해당 계정이 현재 존재합니다."
            res = HttpResponseRedirect(reverse('main:join'))
            messages.error(req, err_msg)
            return res
        
        if pwd1 != pwd2:
            err_msg = "입력하신 비밀번호와 비밀번호 확인이 서로 다릅니다."
            res = HttpResponseRedirect(reverse('main:join'))
            messages.error(req, err_msg)
            return res
        else:
            pwd = make_password(pwd1)
        if not agency_code: #에이전시 계정 발급
            agency_code = ''.join(random.choice(string.digits) for i in range(4))
        else:
            try:
                User.objects.filter(agency_code=agency_code)
            except User.DoesNotExist:
                err_msg = '에이전시 코드 새로 발급됩니다.'
                agency_code = ''.join(random.choice(string.digits) for i in range(4))            
        self_code = ''.join(random.choice(string.ascii_uppercase) for i in range(6))
        s = check_state_from(0)
        user = User(email_account=account, password=pwd, phone=phone, name=name, agency_code=agency_code, recommendation_code=recommendation_code, self_code=self_code, higherarchy=s)
        user.save()        
        try:
            client_ip = ClientIp.objects.get(ip_address=get_client_ip(req))
        except ClientIp.DoesNotExist:
            client_ip = ClientIp(ip_address=get_client_ip(req))
            client_ip.save()
        login_cookie_value = generate_login_cookie(
        account=user, user_agent=req.META['HTTP_USER_AGENT'], ip=client_ip, 
        )
        res = HttpResponseRedirect(reverse('main:login'))        
        # res.set_cookie('login', login_cookie_value, max_age=60 * 60 * 24 * 6, httponly=True)
        return res
        
        
            