import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from main.commonutility import BaseJsonFormat, check_state_from
from main.models.client import State, User
from django.db.models import Q
from main.models.clientdata import RequestTicket
from main.views.security import ParsedClientView

class TicketManage(View):    
    def request_data_about(self, client_obj, ticket_type, count_bool=False):        
        if client_obj.higherarchy.state == 2 and client_obj.is_operator:
            requests = list(RequestTicket.objects.filter(ticket_type=ticket_type).all())            
        elif client_obj.higherarchy.state == 2 and not client_obj.is_operator:
            requests = list(RequestTicket.objects.filter(user__is_operator=False, ticket_type=ticket_type))
        elif client_obj.higherarchy.state == 1:
            requests = list(RequestTicket.objects.filter(user__authorized_by=client_obj, ticket_type=ticket_type))
        else:
            requests = list(RequestTicket.objects.filter(user=client_obj, ticket_type=ticket_type).all())
        if not count_bool:            
            data = [r._request_state for r in requests]     
        else:
            data = [{"count": len(requests)}]
        return BaseJsonFormat(is_success=True, data=data)
    
    @ParsedClientView.init_parse
    def get(self, req):        
        if req.resolver_match.url_name == 'review-ticket':
            res = self.request_data_about(self._client, '리뷰권')
        elif req.resolver_match.url_name == 'purchase-ticket':
            res = self.request_data_about(self._client, '구매권')
        elif req.resolver_match.url_name == 'review-ticket-count':
            res = self.request_data_about(self._client, '리뷰권', count_bool=True)
        elif req.resolver_match.url_name == 'purchase-ticket-count':
            res = self.request_data_about(self._client, '구매권', count_bool=True)        
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def post(self, req):
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            error_msg = '비정상적인 접근입니다'
            res = BaseJsonFormat(is_success=False, error_msg=error_msg)
            res = HttpResponse(res, content_type="application/json", status=401)
            return res
        ids = [int(x) for x in ids]        
        rt_list = RequestTicket.objects.filter(id__in=ids, state__state=0)
        if not rt_list:            
            error_msg = '비정상적인 접근입니다'
            res = BaseJsonFormat(is_success=False, error_msg=error_msg)
            res = HttpResponse(res, content_type="application/json", status=401)
            return res
        if req.resolver_match.url_name == 'reject-ticket-request':
            s = check_state_from(2)
            for rt in rt_list:
                rt.state = s
                rt.save()
            res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
            return HttpResponse(res, content_type="application/json", status=200)        
                
        else:            
            ticket_check = True            
            for rt in rt_list:
                u = User.objects.get(id = rt.user.id)
                if req.resolver_match.url_name == 'review-ticket':
                    if rt.ticket_type != '리뷰권':
                        ticket_check = False
                        break
                    u.review_ticket += rt.count
                                    
                elif req.resolver_match.url_name == 'purchase-ticket':
                    if rt.ticket_type != '구매권':
                        ticket_check = False
                        break
                    u.purchase_ticket += rt.count                
                u.save()
                rt.state = check_state_from(1)
                rt.save()
                
            if not ticket_check:
                error_msg = '비정상적인 요청입니다.'
                res = BaseJsonFormat(is_success=False, error_msg=error_msg)
                res = HttpResponse(res, content_type="application/json", status=401)
                return res
            else:
                res = BaseJsonFormat(is_success=True, msg=f"{rt.ticket_type}이 발급 되었습니다.")
                return HttpResponse(res, content_type="application/json", status=200)        


class UserManage(View):
    def reuest_data_about(self, client_obj, count=False):        
        if client_obj.higherarchy.state == 2 and client_obj.is_operator:
            user_list = list(User.objects.all())
        elif client_obj.higherarchy.state == 2 and not client_obj.is_operator:
            user_list = list(User.objects.filter(~Q(email_account=client_obj.email_account), is_operator=False).all())
        elif client_obj.higherarchy.state == 1:
            user_list = list(User.objects.filter(Q(authorized_by=client_obj)|Q(authorized_by__isnull=True), is_operator=False).all())        
        if count:
            if client_obj.higherarchy.state == 2 and client_obj.is_operator:
                user_list = list(User.objects.filter(authorization=False).all())
            elif client_obj.higherarchy.state == 2 and not client_obj.is_operator:
                user_list = list(User.objects.filter(~Q(email_account=client_obj.email_account)&Q(authorized_by=None), is_operator=False, authorization=False).all())
            elif client_obj.higherarchy.state == 1:
                user_list = list(User.objects.filter(Q(authorized_by=client_obj)|Q(authorized_by=''), is_operator=False, authorization=False).all())        
            return [{"not_authorized_user": len(user_list)}]        
        return user_list
        
    @ParsedClientView.init_parse
    def get(self, req):
        user_list = self.request_data_about(self._client)
        data = [user._user_data for user in user_list]        
        res = BaseJsonFormat(is_success=True, data=data)
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def put(self, req):
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            error_msg = '비정상적인 접근입니다'
            res = BaseJsonFormat(is_success=False, error_msg=error_msg)
            res = HttpResponse(res, content_type="application/json", status=401)
            return res
        ids = [int(x) for x in ids]                
        users = list(User.objects.filter(id__in=ids, authorization=False))
        for u in users:
            u.authorization = True
            u.authorized_by = self._client
            u.save()        
        res = BaseJsonFormat(is_success=True, msg='작업이 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)
    

class ManageIp(View):
    @ParsedClientView.init_parse
    def get(self, req):
        pass
    
    @ParsedClientView.init_parse
    def post(self, req):
        pass

