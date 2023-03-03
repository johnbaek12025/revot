from django.urls import path

from devoperator.views import purchase_info_from, purchase_log_to, review_info_from, review_log_to


app_name = 'devoperator'

urlpatterns = [    
    path('purchase/info/', purchase_info_from, name='give-purchase'), #method: get, data_type:json, data: {"is_success": true, "data":[{"id": "1" ,"pid": "55697421", "mid1": "24445612", "mid2": "244456312", "keyword": "컬러 5셋트 묶음, 겨울양말, 양말나라, 기획전 10종", "purchase_count": 1,"reservation_at_date": "20230222", "reservation_date_at": "1325" "mall_name": "벨킨 공식 네이버", "nid": "jllab001", "npw": "jllab1122", "optionCount": 3, "options": {"option1": "종류", "options2": "색상", "option3": "사이즈"}, ....], "error_msg": null} / data_type:json, data: {"is_success": true, "data": null, "error_msg": null}
    path('purchase/log/', purchase_log_to, name='get-purchase-result'), #method: post, data_type: json, data_exemple: [{"id": "1", "success": True, "ip_address": "172.29.24.114", "try_at_date": "20230222", "try_at": "1324", "done_at": "1325", "done_at_date": "20230222", "nid": 'jllab001', "error_msg": null}, ....] / data_type:json, data: {"is_success": true, "data": null, "error_msg": null}
    path('review/info/', review_info_from, name='give-review'), #data_type:json, data: {"is_success": true, "data": [{"id": "1", "pid": "55697421",  "mid1": "24445612", "mid2": "244456312", "name": "Apple Iphone 11 Pro...", "mall_name": "벨킨 공식 네이버", "img": ["img1", "img2",...], "contents": "반숙 아침에 시간절약 넘 좋아요, 추천합니다. 아침으로 계란후라이만\n먹었는데 이제 온천달걀도 해먹으려구요 ㅎㅎㅎㅎ", "star_count": 3, "reservation_at_date": "20230222", "reservation_at": "1324", },...], "error_msg": null}
    path('review/contents/', review_info_from, name='contents-api'), #data_type:json, data: {"is_success": true, "data": [{"id": "1", "pid": "55697421",  "mid1": "24445612", "mid2": "244456312", "name": "Apple Iphone 11 Pro...", "mall_name": "벨킨 공식 네이버", "img": ["img1", "img2",...], "contents": "반숙 아침에 시간절약 넘 좋아요, 추천합니다. 아침으로 계란후라이만\n먹었는데 이제 온천달걀도 해먹으려구요 ㅎㅎㅎㅎ", "star_count": 3, "reservation_at_date": "20230222", "reservation_at": "1324", },...], "error_msg": null}
    path('review/log/', review_log_to, name='get-review-result'), ##method: post, data_type: json, data_exemple: [{"id": "1", "success": True, "ip_address": "172.29.24.114", "try_at_date": "20230222", "try_at": "13:24", "done_at": "13:25", "done_at_date": "20230222", "nid": 'jllab001', "error_msg": null}, ....] / data_type:json, data: {"is_success": true, "data": null, "error_msg": null}
]