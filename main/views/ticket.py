import json
import re
from django.http import HttpResponse
from django.views import View
from main.commonutility import BaseJsonFormat, check_state_from
from main.models.client import User
from main.models.clientdata import RequestTicket
from main.views.security import ParsedClientView
from django.db import transaction


class AboutTicket(View):    
    def request_data_about(self, ticket_type, count_bool=False):
        requests = list(RequestTicket.objects.filter(ticket_typ=ticket_type, user=self._client).all())        
        if not count_bool:            
            data = [r._request_state for r in requests]
        else:            
            data = [{"count": len(requests)}]
        return BaseJsonFormat(is_success=True, data=data)
    
    @ParsedClientView.init_parse
    def get(self, req):
        if req.resolver_match.url_name == 'review-ticket':
            res = self.request_data_about('리뷰권')
        elif req.resolver_match.url_name == 'purchase-ticket':
            res = self.request_data_about('구매권')
        elif req.resolver_match.url_name == 'review-ticket-count':
            res = self.request_data_about('리뷰권', count_bool=True)
        elif req.resolver_match.url_name == 'purchase-ticket-count':
            res = self.request_data_about('구매권', count_bool=True)                
        return HttpResponse(res, content_type="application/json", status=200)
    
    @transaction.atomic
    @ParsedClientView.init_parse
    def put(self, req):
        data = json.loads(req.body.decode('utf-8'))
        rt_id = int(data['id'])
        rt_cnt = data['cnt']
        try:
            rt = RequestTicket.objects.get(id=rt_id)
        except RequestTicket.DoesNotExist:
            err_msg = '해당 데이터가 존재하지 않습니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)
        
        if rt._request_state['state'] != 0:
            err_msg = '해당 데이터는 삭제가 불가합니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)

        else:
            rt.count = rt_cnt
            rt.save()
        res = BaseJsonFormat(is_success=True, msg='발급 수정이 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)    
    
    
    @transaction.atomic
    @ParsedClientView.init_parse
    def post(self, req):
        data = json.loads(req.body.decode('utf-8'))
        s = check_state_from()
        count = data['count']
        bank = data['bank']
        depositor_name = data['depositor_name']
        
        if req.resolver_match.url_name == 'review-ticket':
            tt='리뷰권'
        else:          
            tt='구매권'  
        rt = RequestTicket(count=count, bank=bank, depositor_name=depositor_name, ticket_type=tt, user=self._client, state=s)
        rt.save()
        res = BaseJsonFormat(is_success=True, msg='신청이 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)
    
    
    @transaction.atomic
    @ParsedClientView.init_parse
    def delete(self, req):
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            err_msg = '비정상 접근입니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)
        ids = [int(x) for x in ids]
        s = check_state_from(0)
        if req.resolver_match.url_name == 'review-ticket':            
            rt = RequestTicket.objects.filter(id__in=ids, ticket_type='리뷰권', user=self._client, state=s)
        else:            
            rt = RequestTicket.objects.get(id__in=ids, ticket_type='구매권', user=self._client, state=s)
        rt.delete()
        res = BaseJsonFormat(is_success=True, msg='삭제가 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)