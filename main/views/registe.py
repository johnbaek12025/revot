import json
from django.http import HttpResponse
from django.views import View
from main.commonutility import BaseJsonFormat, check_state_from
from main.models.client import Product
from main.models.pseudo import Purchase
from main.views.security import ParsedClientView
from datetime import datetime
from django.db.models import Count


class AboutPurchase(View):    
    
    @ParsedClientView.init_parse
    def get(self, req, p_date=None, id=None):        
        if req.resolver_match.url_name == 'date-purchase':
            purchase_list = list(Purchase.objects.filter(product__owner=self._client, reservation_date=p_date).select_related('product'))
            print(purchase_list)
            data = [{
                        "reservation_date": p.reservation_date, 
                        "reservation_at1": p.reservation_at1, 
                        "reservation_at2": p.reservation_at2,
                        "pid": p.product.pid,
                        "mid1": p.product.mid1,
                        "mid2": p.product.mid2, 
                        "state":p.state.state, 
                        "count": p.count,
                        "price": int(p.product.price) * p.count,
                        "options": p.product.options,                        
                        } for p in purchase_list]                    
        elif req.resolver_match.url_name == 'detail':            
            purchase_list = list(Purchase.objects.filter(product__owner=self._client, reservation_date=p_date, id=id).select_related('product'))
            data = [{
                            "reservation_date": p.reservation_date, 
                            "reservation_at": p.reservation_at, 
                            "pid": p.product.pid, 
                            "mid1": p.product.mid1, 
                            "mid2": p.product.mid2, 
                            "state":p.state.state, 
                            "count": p.count,
                            "price": int(p.product.price) * p.count,
                            "options": p.product.options
                            } for p in purchase_list]
        elif req.resolver_match.url_name == 'count':
            data = list(Purchase.objects.values('reservation_date').annotate(count=Count('id')))                        
        res = BaseJsonFormat(is_success=True, data=data)
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def put(self, req):
        data = json.loads(req.body.decode('utf-8'))
        count = data['count']
        reservation_date = data['reservation_date'] #TODO: reservation_at -> rd1, rd2?
        reservation_at = data['reservation_at']        
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def post(self, req):
        today = datetime.now().date()
        data = json.loads(req.body.decode('utf-8'))
        product_id_list = data['product']
        reservation_date = data['reservation_date']
        #TODO: reservation_at randome으로 설정 기능
        reservation_at = data.get('reservation_at', None)        
        count = int(data['count'])        
        s = check_state_from(0)
        rd = datetime.strptime(reservation_date, '%Y-%m-%d').date()        
        if rd < today:
            res = BaseJsonFormat(is_success=False, error_msg=f"선택된 날짜가 과거 입니다.")                
            return HttpResponse(res, content_type="application/json", status=401)
        elif rd == today:
            rt = datetime.strptime(reservation_at, '%H:%M').time()            
            combined_time = datetime.combine(rd, rt)
            if combined_time < datetime.now():
                res = BaseJsonFormat(is_success=False, error_msg=f"선택된 시간이 과거 입니다.")                
                return HttpResponse(res, content_type="application/json", status=401)     
            
        for p_id in product_id_list:            
            self._client.purchase_ticket -= 1
            if self._client.purchase_ticket < 0:
                self._client.purchase_ticket = 0
                self._client.save()    
                res = BaseJsonFormat(is_success=False, error_msg=f"추가 구매권을 구매하시기 바랍니다.")
                return HttpResponse(res, content_type="application/json", status=401)
            self._client.save()
            try:
                p_ob = Product.objects.get(id=p_id)
            except Product.DoesNotExist:
                res = BaseJsonFormat(is_success=False, error_msg=f"해당 상품이 존재하지 않습니다.")
                return HttpResponse(res, content_type="application/json", status=401)
            pp = Purchase(product=p_ob, reservation_date=reservation_date, reservation_at=reservation_at, state=s, count=count)
            pp.save()
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    
    @ParsedClientView.init_parse
    def delete(self, req):
        ids = json.loads(req.body.decode('utf-8'))
        
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)



class AboutReview(View):
    @ParsedClientView.init_parse
    def get(self, req):
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def put(self, req):
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def post(self, req):
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def delete(self, req):
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)