from gettext import translation
import json
import re
from django.views import View
from django.http import HttpResponse
from main.commonutility import BaseJsonFormat, check_state_from
from main.models.client import Product, ProductFolder, State, User
from main.views.product_detail import FetchData
from main.views.security import ParsedClientView
from django.contrib.auth.hashers import make_password
from typing import List, Dict
from django.db import transaction
from django.db.models import Q


class RequestUserInfo(View):
    @ParsedClientView.init_parse
    def get(self, req, display=0):
        if req.resolver_match.url_name == 'update-info':
            res = BaseJsonFormat(is_success=True, data=[self._client._user_join_data])        
        elif req.resolver_match.url_name == 'main':
            res = BaseJsonFormat(is_success=True, data=[self._client._user_data])
        elif req.resolver_match.url_name == 'display-type':
            self._client.display_type = display
            self._client.save()
            res = BaseJsonFormat(is_success=True, data=[self._client._user_data])
        return HttpResponse(res, content_type="application/json", status=200)
    
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
    @ParsedClientView.init_parse
    def get(self, req):
        if req.resolver_match.url_name == 'product':            
            if not Product.objects.filter(owner=self._client).exists():
                res = []
            else:
                res: List[Product] = list(Product.objects.filter(owner=self._client).all())
                res = [r._product_data for r in res]
            res = BaseJsonFormat(is_success=True, data=res)                        
        elif req.resolver_match.url_name == 'product-count':
            if not Product.objects.filter(owner=self._client).exists():
                count = 0
            else:
                count: int = Product.objects.filter(owner=self._client).count()
            res = BaseJsonFormat(is_success=True, data=[{"count": count}])
        return HttpResponse(res, content_type="application/json", status=200)        
    
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
    
    @transaction.atomic            
    @ParsedClientView.init_parse
    def post(self, req):
        if req.resolver_match.url_name == 'product':
            data = json.loads(req.body.decode('utf-8'))            
            url = data['url']
            mid1 = data['mid']
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
            rest_data = fd.main()
            # s = check_state_from(1)
            # p = Product(pid=pid, mid1=mid1, keyword=keyword, state=s, owner=self._client, mall_name=mall_name, **rest_data)
            # p.save()
            res = BaseJsonFormat()
        elif req.resolver_match.url_name == 'product-excel':
            #TODO: excel-format -> List[Dict] and save to Product
            res = BaseJsonFormat(is_success=True, msg='등록이 완료 되었습니다.')
        return HttpResponse(res, content_type="application/json", status=200)
    
    @transaction.atomic
    @ParsedClientView.init_parse
    def delete(self, req):
        ids = json.loads(req.body.decode('utf-8'))['data']
        if not ids:
            err_msg = '비정상 접근입니다.'
            res = BaseJsonFormat(is_success=False, error_msg=err_msg)
            return HttpResponse(res, content_type="application/json", status=401)
        if req.resolver_match.url_name == 'product-delete':
            ids = [int(x) for x in ids]
            p = Product.objects.filter(id__in=ids, owner=self._client, state__state=0)            
            p.delete()            
            res = BaseJsonFormat(is_success=True)
            return HttpResponse(res, content_type="application/json", status=200)
        

class AboutFolder(View):
    @ParsedClientView.init_parse
    def get(self, req, folder_id=None):
        if req.resolver_match.url_name == 'folder':
            folders = list(ProductFolder.objects.filter(user=self._client).all())
            folders = [f._folder_data for f in folders]            
            res = BaseJsonFormat(is_success=True, data=folders)
        elif req.resolver_match.url_name == 'folder-detail':
            try:
                Product.objects.get(owner=self._client, folder=folder_id)
            except Product.DoesNotExist:
                err_msg = "해당 폴더가 존재하지 않습니다."
                res = BaseJsonFormat(is_success=False, error_msg=err_msg)    
            else:
                products = list(Product.objects.filter(owner=self._client, folder=folder_id).all())
                product_list = [p._product_data for p in products]
                res = BaseJsonFormat(is_success=True, data=product_list)
        return HttpResponse(res, content_type="application/json", status=200)
    
    @transaction.atomic
    @ParsedClientView.init_parse
    def put(self, req):
        data = json.loads(req.body.decode('utf-8'))
        print(data)
        f_id = data['id']
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
    def post(self, req):
        data = json.loads(req.body)
        ProductFolder(user=self._client).save()        
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
    
   