from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from main.commonutility import BaseJsonFormat


@csrf_exempt
def purchase_info_from(req):
    if req.method == 'GET':
        res = BaseJsonFormat(is_success=True)
        res = HttpResponse(res, content_type="application/json")

@csrf_exempt
def purchase_log_to(req):
    if req.method == 'POST':
        res = BaseJsonFormat(is_success=True)
        res = HttpResponse(res, content_type="application/json")

@csrf_exempt        
def review_info_from(req):
    if req.method == 'GET':
        res = BaseJsonFormat(is_success=True)
        res = HttpResponse(res, content_type="application/json")
        
@csrf_exempt
def review_log_to(req):
    if req.method == 'GET':
        res = BaseJsonFormat(is_success=True)
        res = HttpResponse(res, content_type="application/json")