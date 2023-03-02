from django.urls import path
from main.models.client import User
from main.views.clientdata import AboutProduct, ProductData, RequestUserInfo, AboutFolder
from main.views.pageviews import MainPage, MainPageGrid, MyPage, PurchaseMainPage, PurchaseSchedulePage, ReviewPage, ReviewSchedulePage
from main.views.registe import AboutPurchase, AboutReview
from main.views.ticket import AboutTicket
from main.views.join import JoinPage
from main.views.login import LogIn, LogOut
from main.views.security import LoggedIn, LoggedOut


app_name = 'main'

urlpatterns = [    
    path('', LoggedOut()(LogIn.as_view(http_method_names=['get', 'post'])), name='login'),
    path('join/', LoggedOut()(JoinPage.as_view(http_method_names=['get', 'post'])), name='join'),
    path('logout/', LoggedIn()(LogOut.as_view(http_method_names=['get'])), name='logout'),
    path('mypage/', LoggedIn()(MyPage.as_view(http_method_names=['get'])), name='mypage'),
    path('mainpage/', LoggedIn()(MainPage.as_view(http_method_names=['get'])), name='main'),
    path('mainpage/grid/', LoggedIn()(MainPageGrid.as_view(http_method_names=['get'])), name='main-grid'),
    path('buypage/', LoggedIn()(PurchaseMainPage.as_view(http_method_names=['get'])), name='buy-page'),
    path('buypage/schecule/', LoggedIn()(PurchaseSchedulePage.as_view(http_method_names=['get'])), name='buy-schedule'),
    path('reviewpage/', LoggedIn()(ReviewPage.as_view(http_method_names=['get'])), name='review-page'),
    path('reviewpage/schedule/', LoggedIn()(ReviewSchedulePage.as_view(http_method_names=['get'])), name='review-schedule'),
    path('mainpage/<int:folder_id>/', LoggedIn()(MainPage.as_view(http_method_names=['get'])), name='folder-page'),
    
    
    path('user/info/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get', 'put'])), name='my-data'),
    path('user/info/<int:display>/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get'])), name='display-type'),        
    path('user/newfolder/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='new-folder'),
    path('user/product/', LoggedIn()(ProductData.as_view(http_method_names=['get'])), name='product-all'),
    path('user/product/', LoggedIn()(ProductData.as_view(http_method_names=['get','put','post'])), name='product-all'),
    path('user/product/delete/', AboutProduct.as_view(http_method_names=['delete']), name='product-delete'),
    path('user/product/count/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='product'),
    # path('user/product/excel/', LoggedIn()(AboutProduct.as_view(http_method_names=['post'])), name='product-excel'),
    path('user/folder/', LoggedIn()(AboutFolder.as_view(http_method_names=['get', 'put'])), name='folder'),
    
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

