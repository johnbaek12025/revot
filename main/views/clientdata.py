from gettext import translation
import json
import re
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from main.commonutility import BaseJsonFormat, check_state_from
from main.models.client import Product, ProductFolder
from main.views.exceptions import DataValueEmpty
from main.views.product_detail import FetchData
from main.views.security import ParsedClientView
from django.contrib.auth.hashers import make_password
from typing import List, Dict
from django.db import transaction
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


class RequestUserInfo(View):
    @ParsedClientView.init_parse
    def get(self, req, display=0):
        if req.resolver_match.url_name == 'my-data-detail':
            data = {}
            data.update(self._client._user_data_detail)
            data['AE_NAME']= self._client.authorized_by.name
            data['AE_phone']= self._client.authorized_by.phone
            res = BaseJsonFormat(is_success=True, data=data)
            return HttpResponse(res, content_type="application/json", status=200)
        
        elif req.resolver_match.url_name == 'my-ticket':            
            res = BaseJsonFormat(is_success=True, data=self._client._user_tickets)
            return HttpResponse(res, content_type="application/json", status=200)
    
    @csrf_exempt
    @transaction.atomic
    @ParsedClientView.init_parse        
    def put(self, req):        
        if req.resolver_match.url_name == 'update-info':
            data = json.loads(req.body.decode('utf-8'))
            pwd1 = data['pwd1']
            pwd2 = data['pwd2']
            if pwd1 != pwd2:
                err_msg = "입력하신 비밀번호와 비밀번호 확인이 서로 다릅니다."
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=403)
            else:
                pwd = make_password(pwd1)
            self._client.password = pwd
            self._client.save()
            res = BaseJsonFormat()
        else:
            res = BaseJsonFormat()
        return HttpResponse(res, content_type="application/json", status=200)



class AboutProduct(View):    
    def jsonize_specific_data(self, req, q):
        product_list = list(Product.objects.filter(q))
        products_data = []
        for p in product_list:
            keywords = [k for k in p.keyword.split(', ')]            
            if p.options:                                
                try:
                    options = json.loads(p.options)
                    option_count = options['option_count']
                except TypeError:
                    options = json.loads(json.loads(p.options))
                    option_count = options['option_count']
                option_kind = list(options['options'].keys())
            else:
                option_kind = []
                option_count = 0
            products_data.append({
                                    "id": p.id,
                                    "name": p.name, 
                                    "mall_name": p.mall_name, 
                                    "birth": p.birth.strftime('%Y-%m-%d'),
                                    "keyword": keywords,
                                    "mid1": p.mid1,
                                    "mid2": p.mid2,
                                    "pid": p.pid,
                                    "img": p.img_url,
                                    "searching_type": p.searching_type,
                                    "option_count": option_count,
                                    "options": option_kind,
                                })
        pg_num = req.GET.get('page', 1)        
        sc = req.GET.get('sc', 10)
        paginator = Paginator(products_data, per_page=sc)
        page_obj = paginator.get_page(pg_num)        
        return BaseJsonFormat(is_success=True, data=list(page_obj.object_list))
    
    @ParsedClientView.init_parse
    def get(self, req, p_id=None):
        if req.resolver_match.url_name == 'product-count':
            if not Product.objects.filter(owner=self._client).exists():
                s_count = 0
                f_count = 0
            else:
                s = check_state_from(1)
                s_count: int = Product.objects.filter(owner=self._client, state=s).count()
                f = check_state_from(2)
                f_count: int = Product.objects.filter(owner=self._client, state=f).count()
            products_data = {"total": s_count + f_count, "success_count": s_count, "fail_count": f_count}
            res = BaseJsonFormat(is_success=True, data=products_data)          
        elif req.resolver_match.url_name == 'total-product':         
            q = Q(owner=self._client)
            res = self.jsonize_specific_data(req, q)            
        elif req.resolver_match.url_name == 'success-product':
            s = check_state_from(1)
            q = Q(owner=self._client) & Q(state=s)
            res = self.jsonize_specific_data(req, q)
        elif req.resolver_match.url_name == 'fail-product':
            s = check_state_from(2)
            q = Q(owner=self._client) & Q(state=s)
            res = self.jsonize_specific_data(req, q)        
        elif req.resolver_match.url_name == 'product-detail':
            try:
                p = Product.objects.get(id=p_id)
            except Product.DoesNotExist:
                err_msg = '비정상 접근입니다.'
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)        
            else:
                try:
                    options = json.loads(p.options)
                    option_count = options['option_count']
                except TypeError:
                    options = json.loads(json.loads(p.options))
                    option_count = options['option_count']
                options = options['options']                              
                keywords = [k for k in p.keyword.split(', ')]
                data = {
                    "id": p.id,
                    "name": p.name, 
                    "mall_name": p.mall_name, 
                    "birth": p.birth.strftime('%Y-%m-%d'),
                    "keyword": keywords,
                    "mid1": p.mid1,
                    "mid2": p.mid2,
                    "pid": p.pid,
                    "img": p.img_url,
                    "option_count": option_count,                    
                    "option_detail": options,
                    "searching_type": p.searching_type,
                }
                res = BaseJsonFormat(is_success=True, data=data)
        elif req.resolver_match.url_name == 'search-product':
            query = req.GET.get('q')            
            q = Q(owner=self._client) & Q(name__icontains=query)
            res = self.jsonize_specific_data(req, q)            
        elif req.resolver_match.url_name == 'product-delete':
            try:
                p = Product.objects.get(id=p_id)
            except Product.DoesNotExist:
                err_msg = '비정상 접근입니다.'
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)        
            else:
                p.delete()
                p.save()
            res = BaseJsonFormat(is_success=True, msg='정상으로 삭제 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)
    
    @csrf_exempt
    @transaction.atomic        
    @ParsedClientView.init_parse
    def put(self, req):
        if req.resolver_match.url_name == 'product':
            data = json.loads(req.body.decode('utf-8'))
            url = data['url']
            mid1 = data['mid']
            keyword = data['keyword']
            url = re.sub(r'\?.+', '', url)
            pid = re.sub(r'[^0-9+]', '', url)
            try:
                p = Product.objects.get(owner=self._client, pid=pid)
            except Product.DoesNotExist:
                err_msg = "해당 상품이 존재하지 않습니다."
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=404)
            p.pid = pid
            p.mid1 = mid1
            p.keyword = keyword
            p.save()
            res = BaseJsonFormat(is_success=True)
            return HttpResponse(res, content_type="application/json", status=200)
    
    @csrf_exempt
    @transaction.atomic            
    @ParsedClientView.init_parse
    def post(self, req):
        if req.resolver_match.url_name == 'product':
            data = json.loads(req.body.decode('utf-8'))
            url = data['url']
            mid1 = data['mid1']
            mid2 = data.get('mid2', None)
            keyword = data['keyword']            
            match = re.match(r"https:\/\/smartstore\.naver\.com\/(\w+)\/products\/(\d+)\?*.*", url)                     
            if match:
                mall_name = match.group(1)
                pid = match.group(2)
            else:                
                err_msg = '등록된 url을 다시 확인해주세요.'
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)
            fd = FetchData(mall_name=mall_name, pid=pid)
            try:
                rest_data = fd.main()
            except DataValueEmpty:
                s = check_state_from(2)                
                p = Product(pid=pid, mid1=mid1, mid2=mid2, keyword=keyword, state=s, owner=self._client, mall_name=mall_name)
                p.save()
                res = BaseJsonFormat(is_success=False, error_msg='상품에 대한 정보를 찾을 수 없습니다.')
                return HttpResponse(res, content_type="application/json", status=401)
            else:
                s = check_state_from(1)
                p = Product(pid=pid, mid1=mid1, mid2=mid2, keyword=keyword, state=s, owner=self._client, mall_name=mall_name, **rest_data)
                p.save()
                res = BaseJsonFormat()
        elif req.resolver_match.url_name == 'product-excel':
        #     #TODO: excel-format -> List[Dict] and save to Product
            res = BaseJsonFormat(is_success=True, msg='등록이 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)
    
        
    @transaction.atomic
    @ParsedClientView.init_parse
    def delete(self, req):
        if req.resolver_match.url_name == 'products-delete':
            ids = json.loads(req.body.decode('utf-8'))['data']
            print(ids)
            if not ids:
                err_msg = '비정상 접근입니다.'
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)            
            ids = [int(x) for x in ids]
            p = Product.objects.filter(id__in=ids, owner=self._client, state__state=0)            
            p.delete()            
            res = BaseJsonFormat(is_success=True, msg='정상으로 삭제 되었습니다.')
            return HttpResponse(res, content_type="application/json", status=200)


class AboutFolder(View):
    def jsonize_specific_data(self, req, q):
        product_list = list(Product.objects.filter(q))      
        products_data = []
        for p in product_list:
            keywords = [k for k in p.keyword.split(', ')]            
            if p.options:                
                try:
                    options = json.loads(p.options)
                    option_count = options['option_count']
                except TypeError:
                    options = json.loads(json.loads(p.options))
                    option_count = options['option_count']
                option_kind = list(options['options'].keys())
            else:
                option_kind = []
                option_count = 0
            products_data.append({
                                    "id": p.id,
                                    "name": p.name, 
                                    "mall_name": p.mall_name, 
                                    "birth": p.birth.strftime('%Y-%m-%d'),
                                    "keyword": keywords,
                                    "mid1": p.mid1,
                                    "mid2": p.mid2,
                                    "pid": p.pid,
                                    "img": p.img_url,
                                    "searching_type": p.searching_type,
                                    "option_count": option_count,
                                    "options": option_kind,
                                })
        pg_num = req.GET.get('page', 1)        
        sc = req.GET.get('sc', 10)
        paginator = Paginator(products_data, per_page=sc)
        page_obj = paginator.get_page(pg_num)        
        return BaseJsonFormat(is_success=True, data=list(page_obj.object_list))
    
    @ParsedClientView.init_parse
    def get(self, req, folder_id=None, p_id=None):        
        if req.resolver_match.url_name == 'folder-product':
            q = Q(owner=self._client) & Q(folder=folder_id)
            res = self.jsonize_specific_data(req, q)
        elif req.resolver_match.url_name == 'folder-product-detail':
            try:
                p = Product.objects.get(Q(id=p_id)&Q(folder=folder_id))
            except Product.DoesNotExist:
                err_msg = '비정상 접근입니다.'
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)
                return HttpResponse(res, content_type="application/json", status=401)        
            else:
                try:
                    options = json.loads(p.options)
                    option_count = options['option_count']
                except TypeError:
                    options = json.loads(json.loads(p.options))
                    option_count = options['option_count']                
                options = options['options']                            
                keywords = [k for k in p.keyword.split(', ')]
                data = {
                    "id": p.id,
                    "name": p.name, 
                    "mall_name": p.mall_name, 
                    "birth": p.birth.strftime('%Y-%m-%d'),
                    "keyword": keywords,
                    "mid1": p.mid1,
                    "mid2": p.mid2,
                    "pid": p.pid,
                    "img": p.img_url,
                    "option_count": option_count,                    
                    "option_detail": options,
                    "searching_type": p.searching_type,
                }
                res = BaseJsonFormat(is_success=True, data=data)
        elif req.resolver_match.url_name == 'folder-search-product':
            query = req.GET.get('q')
            q = Q(owner=self._client) & Q(name__icontains=query)&Q(folder=folder_id)
            res = self.jsonize_specific_data(req, q)        
        elif req.resolver_match.url_name == 'folder-detail-count':
            p_cnt = Product.objects.filter(Q(owner=self._client)& Q(folder__id=folder_id)).count()
            res = BaseJsonFormat(is_success=True, data={"products_cnt": p_cnt})
        elif req.resolver_match.url_name == 'new-folder':
            referer = req.META.get('HTTP_REFERER')            
            ProductFolder(user=self._client).save()
            return redirect(referer)        
        return HttpResponse(res, content_type="application/json", status=200)
        
    @csrf_exempt 
    @transaction.atomic
    @ParsedClientView.init_parse
    def put(self, req):
        data = json.loads(req.body.decode('utf-8'))
        print(data)
        f_id = int(data['id'])
        name = data.get("name", None)
        product_id_list = data['product']
        folder = ProductFolder.objects.get(id=f_id, user=self._client)        
        if name:
            folder.name = name 
        products = list(Product.objects.filter(id__in=product_id_list).all())
        pf = ProductFolder.objects.get(user=self._client, id=f_id)
        for p in products:
            p.folder = pf
            p.save()            
        res = BaseJsonFormat(is_success=True)
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
        pf = ProductFolder.objects.filter(id__in=ids, user=self._client)
        pf.delete()
        res = BaseJsonFormat(is_success=True)
        return HttpResponse(res, content_type="application/json", status=200)
    
   
