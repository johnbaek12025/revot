from django.urls import path
from main.models.client import User
from main.views.clientdata import AboutProduct, RequestUserInfo, AboutFolder
from main.views.registe import AboutPurchase, AboutReview
from main.views.ticket import AboutTicket
from main.views.join import JoinPage
from main.views.login import LogIn, LogOut
from main.views.security import LoggedIn, LoggedOut


app_name = 'main'

urlpatterns = [    
    path('join/', LoggedOut()(JoinPage.as_view(http_method_names=['get', 'post'])), name='join'),
    path('login/', LoggedOut()(LogIn.as_view(http_method_names=['get', 'post'])), name='login'),
    path('logout/', LoggedIn()(LogOut.as_view(http_method_names=['get'])), name='logout'),
    path('user/info/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get', 'put'])), name='update-info'),
    path('user/info/<int:display>/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get'])), name='display-type'),
    path('main/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get'])), name='main'),
    path('user/product/', LoggedIn()(AboutProduct.as_view(http_method_names=['get', 'put','post'])), name='product'),
    path('user/product/delete/', AboutProduct.as_view(http_method_names=['delete']), name='product-delete'),
    path('user/product/count/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='product-count'),
    path('user/product/excel/', LoggedIn()(AboutProduct.as_view(http_method_names=['post'])), name='product-excel'),
    path('user/folder/', LoggedIn()(AboutFolder.as_view(http_method_names=['get', 'put', 'post'])), name='folder'),
    path('user/folder/detail/<int:folder_id>/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-detail'),
    path('user/folder/delete/', LoggedIn()(AboutFolder.as_view(http_method_names=['delete'])), name='folder-delete'),
    path('history/review/request/', LoggedIn()(AboutTicket.as_view(http_method_names=['get', 'put'])), name='review-ticket'),
    path('history/purchase/request/', LoggedIn()(AboutTicket.as_view(http_method_names=['get', 'put'])), name='purchase-ticket'),
    path('history/review/request/count/', LoggedIn()(AboutTicket.as_view(http_method_names=['get'])), name='review-ticket-count'),
    path('history/purchase/request/count/', LoggedIn()(AboutTicket.as_view(http_method_names=['get'])), name='purchase-ticket-count'),
    path('request/review/ticket/', LoggedIn()(AboutTicket.as_view(http_method_names=['post'])), name='review-ticket'),
    path('request/purchase/ticket/', LoggedIn()(AboutTicket.as_view(http_method_names=['post'])), name='purchase-ticket'),    
    path('request/review/ticket/delete/', LoggedIn()(AboutTicket.as_view(http_method_names=['delete'])), name='review-ticket'),
    path('request/purchase/ticket/delete/', LoggedIn()(AboutTicket.as_view(http_method_names=['delete'])), name='purchase-ticket'),
    
    path('purchase/count/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='count'),
    path('history/purchase/<str:p_date>/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='date-purchase'),
    path('detail/purchase/<str:p_date>/info/<str:id>/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='detail'),
    path('purchase/update/', LoggedIn()(AboutPurchase.as_view(http_method_names=['put'])), name='purchase-update'),
    path('registe/purchase/', LoggedIn()(AboutPurchase.as_view(http_method_names=['post'])), name='purchase'),
    path('delete/purchase/', LoggedIn()(AboutPurchase.as_view(http_method_names=['delete'])), name='delete-purchase'),
    
    path('review/count/',LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='count'),
    path('history/review//<str:p_date>/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='total-purchase'),
    path('detail/review/<str:date>/info/<str:id>/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='detail'),    
    path('review/update/', LoggedIn()(AboutReview.as_view(http_method_names=['put'])), name='review-update'),
    path('registe/review/', LoggedIn()(AboutReview.as_view(http_method_names=['post'])), name='review'),
    path('rgiste/img/', LoggedIn()(AboutReview.as_view(http_method_names=['post'])), name='review-img'),
    path('delete/review/', LoggedIn()(AboutPurchase.as_view(http_method_names=['delete'])), name='delete-purchase'),
]

