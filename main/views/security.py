from datetime import timedelta
from functools import wraps
import functools
import random
import string
from typing import List
from django.db import IntegrityError
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from main.models.client import ProductFolder, User
from main.models.security import LoginSession
from main.commonutility import BaseJsonFormat, check_state_from
from main.views.exceptions import NotParsedError, SessionCookieNonExists, SessionExpiration, SessionValueWrong
from django.utils.timezone import now


class LoggedOut:
    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # get reg from args or kwargs
            req = kwargs.get('req', None)            
            if not req:
                req = args[0]  # why 1? => instance_method(self, req, *args, **kwargs)

            # check if there is login cookie value
            login_cookie = req.COOKIES.get('login', None)
            if login_cookie:                
                return HttpResponseRedirect(reverse('main:main'))
                

            # if it is, progress next logic
            return func(*args, **kwargs)

        return wrapper


class LoggedIn:

    def __init__(self, hierarchies:List[int]=None, operator:bool=False):
        self.hierarchies = hierarchies
        self.operator = operator
        
    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):            
            # get req obj            
            req = None
            for k, v in kwargs.items():
                if isinstance(v, HttpRequest):
                    req = v
                    break

            for arg in args:
                if isinstance(arg, HttpRequest):
                    req = arg
                    break            
            if req is None:
                raise Exception('req 인자를 찾지 못하였습니다.')
            res = HttpResponseRedirect(reverse('main:login'))

            try:                
                client = get_client_object(req=req)                
            except (SessionCookieNonExists, SessionValueWrong):
                res.delete_cookie('login')  # 여기서는 필히 해줘야함
                return res
            except SessionExpiration:
                res.delete_cookie('login')
                return res
            if client is None or not client.authorization:
                res.delete_cookie('login')
                res = HttpResponseRedirect(reverse('main:login'))
                return res            
            
            if self.hierarchies:
                if client.higherarchy.state not in self.hierarchies :
                    res = HttpResponseRedirect(reverse('main:main'))
                    return res
                else:
                    if self.operator:
                        if getattr(client, 'is_operator', False):
                            client_cls = client.__class__
                        else:
                            res = HttpResponseRedirect(reverse('main:main'))
                            return res
                    else:
                        client_cls = client.__class__                        
            
            return func(*args, **kwargs)

        return wrapper


def get_client_object(account=None, req=None, session_birth_within=7):    
    if (account, req) == (None, None):
        raise ValueError('account, req 둘 중 최소 하나는 입력해줘야 합니다.')

    if req and account is None:
        try:
            login_session_value = req.COOKIES['login']
        except KeyError:
            raise SessionCookieNonExists
        else:
            try:
                login_session = LoginSession.objects.get(value=login_session_value, logged_out=False)
                account = login_session.account
            except LoginSession.DoesNotExist:
                raise SessionValueWrong
            else:
                try:
                    login_session = LoginSession.objects.get(
                        value=login_session_value,
                        birth__gte=now()-timedelta(days=session_birth_within)
                    )
                except LoginSession.DoesNotExist:
                    raise SessionExpiration
    return account

def generate_login_cookie(account, user_agent, ip, session_cls=LoginSession):
    
    while True:
        try:
            login_cookie_value = ''.join(
                random.choices(string.ascii_letters + string.digits, k=random.randint(60, 70)))
        except AttributeError:

            def random_choices(p, k):  # random.choices -> 3.6 up, so this func is for 3.5 down
                temp = []
                for _ in range(k):
                    temp.append(p[random.randrange(len(p))])
                return temp

            login_cookie_value = ''.join(
                random_choices(string.ascii_letters + string.digits, k=random.randint(60, 70)))        
        try:
            session_cls(
                account=account,
                value=login_cookie_value,
                user_agent=user_agent,
                logged_out=False,
                ip=ip,
            ).save()
        except IntegrityError('sesseion value overlaps, retry to create and save'):        
            continue
        else:
            break

    return login_cookie_value
    


class ParsedClientView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = None

    @staticmethod
    def init_parse(fun):

        @functools.wraps(fun)
        def wrapper(*args, **kwargs):            
            instance = args[0]            
            req = kwargs.get('req', None) or args[1]
            try:
                client_obj = get_client_object(req=req)
            except (SessionCookieNonExists, SessionValueWrong):
                #  # 체커 봇, 랭커 봇인 경우
                # if 'encoded' in kwargs:
                #     setattr(instance, '_client', User.objects.filter(is_operator=True)[:1].get())
                res = BaseJsonFormat(is_success=False, error_msg='세션이 없거나 잘못된 세션값입니다.')
                res = HttpResponse(res, content_type="application/json", status=401)
                return res
            else:
                setattr(instance, '_client', client_obj)
            return fun(*args, **kwargs)        
        return wrapper
    
    @property
    def client(self):
        if self._client is None:
            raise NotParsedError
        return self._client
    
    