import json
from django.db import OperationalError

from django.http import HttpResponse
from django.views import View
from main.commonutility import BaseJsonFormat, check_state_from, random_date
from main.models.client import Product
from main.models.pseudo import Image, Purchase, Review
from main.views.security import ParsedClientView
from datetime import datetime
from django.db.models import Count
from django.db.models import F
from django.core.paginator import Paginator
from django.db.models import Q



class AboutPurchase(View):    
    def make_pagination(self, req, data:list):
        data = [{
                    "id": p.id,
                    "reservation_date": p.reservation_date, 
                    "reservation_at": p.reservation_at, 
                    "done_time": p.done,
                    "pid": p.product.pid,
                    "mid1": p.product.mid1,
                    "mid2": p.product.mid2, 
                    "state":p.state.state, 
                    "count": p.count,
                    "price": int(p.product.price) * p.count,
                    "options": json.loads(p.selected_options),                    
                    "option_count": json.loads(p.product.options)['option_count'],
                    } for p in data]
        pg_num = req.GET.get('page', 1)        
        sc = req.GET.get('sc', 10)
        paginator = Paginator(data, per_page=sc)
        page_obj = paginator.get_page(pg_num)
        data = list(page_obj.object_list)          
        return data
    
    @ParsedClientView.init_parse
    def get(self, req, p_date=None, id=None):        
        if req.resolver_match.url_name == 'date-purchase':
            purchase_list = list(Purchase.objects.filter(Q(product__owner=self._client)&Q(reservation_date=p_date)).select_related('product'))
            data = self.make_pagination(req, purchase_list)
        elif req.resolver_match.url_name == 'detail':            
            purchase_list= list(Purchase.objects.filter(product__owner=self._client, reservation_date=p_date, id=int(id)).select_related('product'))
            data = self.make_pagination(req, purchase_list)
        elif req.resolver_match.url_name == 'date-count':
            data = list(Purchase.objects.filter(Q(product__owner=self._client)).values('reservation_date', state_name=F('state__state')).annotate(count=Count('id')))
        elif req.resolver_match.url_name == 'state-count':
            i = check_state_from(0)
            s = check_state_from(1)
            f = check_state_from(2)
            p_cnt = Purchase.objects.filter(Q(product__owner=self._client)&Q(state=i)).count()
            s_cnt = Purchase.objects.filter(Q(product__owner=self._client)&Q(state=s)).count()
            f_cnt = Purchase.objects.filter(Q(product__owner=self._client)&Q(state=f)).count()            
            data = {"total": p_cnt+s_cnt+f_cnt,"progress": p_cnt, "success": s_cnt, "fail": f_cnt}
        elif req.resolver_match.url_name == 'total':            
            purchase_list = list(Purchase.objects.filter(product__owner=self._client))            
            print(purchase_list)
            data = self.make_pagination(req, purchase_list)
        elif req.resolver_match.url_name == 'success':            
            s = check_state_from(1)            
            purchase_list = list(Purchase.objects.filter(Q(product__owner=self._client)&Q(state=s)))            
            data = self.make_pagination(req, purchase_list)
        elif req.resolver_match.url_name == 'progress':
            p = check_state_from(0)
            purchase_list = list(Purchase.objects.filter(Q(product__owner=self._client)&Q(state=p)))
            data = self.make_pagination(req, purchase_list)
        elif req.resolver_match.url_name == 'fail':
            f = check_state_from(2)
            purchase_list = list(Purchase.objects.filter(Q(product__owner=self._client)&Q(state=f)))
            data = self.make_pagination(req, purchase_list)
        res = BaseJsonFormat(is_success=True, data=data)
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def put(self, req):
        data = json.loads(req.body.decode('utf-8'))
        id = data['id']
        count = data['count']
        reservation_date = data['reservation_date']        
        reservation_at = data['reservation_at']
        try:
            rp = Purchase.objects.get(id=id)
        except Purchase.DoesNotExist:
            res = BaseJsonFormat(is_success=True, msg=f"비정상 접근입니다.")
            return HttpResponse(res, content_type="application/json", status=401)
        rp.count = count
        rp.reservation_date = reservation_date
        rp.reservation_at = reservation_at
        rp.save()
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def post(self, req):        
        data = json.loads(req.body.decode('utf-8'))
        print(data)    
        p_id = data['product']        
        selected_options = data['options']
        count = int(data['count'])        
        rd = data['reservation_date']
        rt1 = data.get('rt1', None)
        rt2 = data.get('rt2', None)
        cd, ct = datetime.now().strftime('%Y-%m-%d %H:%M').split(' ')        
        if rd == cd:
            if rt1 and rt2:
                d1 = datetime.strptime(f"{cd} {rt1}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{cd} {rt2}", '%Y-%m-%d %H:%M')
            else:                
                d1 = datetime.strptime(f"{cd} {ct}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{cd} 23:59", '%Y-%m-%d %H:%M')                
        elif rd < cd:
            res = BaseJsonFormat(is_success=False, error_msg=f"선택된 날짜가 과거 입니다.")                
            return HttpResponse(res, content_type="application/json", status=401)
        else:                   
            if rt1 and rt2:
                d1 = datetime.strptime(f"{rd} {rt1}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{rd} {rt2}", '%Y-%m-%d %H:%M')
            else:                
                d1 = datetime.strptime(f"{rd} 00:00", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{rd} 23:59", '%Y-%m-%d %H:%M')            
        rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')
        s = check_state_from(0)        
        self._client.purchase_ticket -= 1
        if self._client.purchase_ticket < 0:            
            res = BaseJsonFormat(is_success=False, error_msg=f"추가 구매권을 구매하시기 바랍니다.")
            return HttpResponse(res, content_type="application/json", status=401)            
        try:
            p_ob = Product.objects.get(id=p_id, owner=self._client)
        except Product.DoesNotExist:
            res = BaseJsonFormat(is_success=False, error_msg=f"해당 상품이 존재하지 않습니다.")
            return HttpResponse(res, content_type="application/json", status=401)
        
        pp = Purchase(product=p_ob, reservation_date=rd, reservation_at=rt, state=s, count=count, selected_options=selected_options)
        pp.save()
        print(pp)
        self._client.save()
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    
    @ParsedClientView.init_parse
    def delete(self, req):        
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            err_msg = '비정상 접근입니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)        
        ids = [int(x) for x in ids]
        s = check_state_from(0)
        ph = Purchase.objects.filter(id__in=ids, product__owner=self._client, state=s)
        ph.delete()
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)



class AboutReview(View):
    @ParsedClientView.init_parse
    def get(self, req):
        if req.resolver_match.url_name == 'date-count':
            pass
        elif req.resolver_match.url_name == 'date-review':
            pass
        elif req.resolver_match.url_name == 'state-count':
            i = check_state_from(0)
            s = check_state_from(1)
            f = check_state_from(2)
            p_cnt = Review.objects.filter(Q(product__owner=self._client)&Q(state=i)).count()
            s_cnt = Review.objects.filter(Q(product__owner=self._client)&Q(state=s)).count()
            f_cnt = Review.objects.filter(Q(product__owner=self._client)&Q(state=f)).count()            
            data = {"total": p_cnt+s_cnt+f_cnt,"progress": p_cnt, "success": s_cnt, "fail": f_cnt}
        elif req.resolver_match.url_name == 'detail':
            pass
        elif req.resolver_match.url_name == 'total':
            pass
        elif req.resolver_match.url_name == 'progress':
            pass
        elif req.resolver_match.url_name == 'fail':
            pass
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.", data=data)
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def put(self, req):
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def post(self, req):
        print(self._client)
        files = req.FILES['file']
        data = json.loads(req.body.decode('utf-8'))
        auto_fill = data.get('auto_fill', False)
        r_contents = data.get('review', None)
        purchase_id = int(data['purchase'])
        rd = data['reservation_date']
        rt1 = data.get('rt1', None)
        rt2 = data.get('rt2', None)
        cd, ct = datetime.now().strftime('%Y-%m-%d %H:%M').split(' ')        
        if rd == cd:
            if rt1 and rt2:
                d1 = datetime.strptime(f"{cd} {rt1}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{cd} {rt2}", '%Y-%m-%d %H:%M')
            else:
                d1 = datetime.strptime(f"{cd} {ct}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{cd} 23:59", '%Y-%m-%d %H:%M')
        elif rd < cd:
            res = BaseJsonFormat(is_success=False, error_msg=f"선택된 날짜가 과거 입니다.")
            return HttpResponse(res, content_type="application/json", status=401)
        else:
            if rt1 and rt2:
                d1 = datetime.strptime(f"{rd} {rt1}", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{rd} {rt2}", '%Y-%m-%d %H:%M')
            else:
                d1 = datetime.strptime(f"{rd} 00:00", '%Y-%m-%d %H:%M')
                d2 = datetime.strptime(f"{rd} 23:59", '%Y-%m-%d %H:%M')
        rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')
        s = check_state_from(0)
        try:
            po = Purchase.objects.get(id=purchase_id)
        except Purchase.DoesNotExist:
            res = BaseJsonFormat(is_success=False, error_msg=f"해당 상품이 존재하지 않습니다.")
            return HttpResponse(res, content_type="application/json", status=401)        
        
        if not auto_fill:
            contents = r_contents
        else:
            contents = None
            #TODO: implement api for getting review content from outer service
        r = Review(purchase=po, reservation_at=rd, reservation_date=rt, state=s, contents=contents)
        r.save()
        for f in files:
            i = Image(img=f, review=r)
            i.save()        
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)
    
    @ParsedClientView.init_parse
    def delete(self, req):
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            err_msg = '비정상 접근입니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)        
        ids = [int(x) for x in ids]
        s = check_state_from(0)
        ph = Review.objects.filter(id__in=ids, purchase__product__owner=self._client, state=s)
        ph.delete()
        res = BaseJsonFormat(is_success=True, msg=f"작업이 완료 되었습니다.")
        return HttpResponse(res, content_type="application/json", status=200)