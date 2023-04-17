from django.urls import path
from main.models.client import User
from main.views.clientdata import AboutProduct, RequestUserInfo, AboutFolder
from main.views.pageviews import FolderPage, MainPage, MainPageGrid, MyPage, PurchaseMainPage, PurchaseSchedulePage, ReviewPage, ReviewSchedulePage
from main.views.registe import AboutPurchase, AboutReview, Revot
from main.views.ticket import AboutTicket
from main.views.join import JoinPage
from main.views.login import LogIn, LogOut
from main.views.login2 import LogIn2
from main.views.security import LoggedIn, LoggedOut


app_name = 'main'

urlpatterns = [    
    path('login/', LoggedOut()(LogIn2.as_view(http_method_names=['get', 'post'])), name='login2'),
    path('join/', LoggedOut()(JoinPage.as_view(http_method_names=['get', 'post'])), name='join'),
    path('logout/', LoggedIn()(LogOut.as_view(http_method_names=['get'])), name='logout'),
    path('mypage/', LoggedIn()(MyPage.as_view(http_method_names=['get'])), name='mypage'),
    path('mainpage/', LoggedIn()(MainPage.as_view(http_method_names=['get'])), name='main'),
    path('mainpage/grid/', LoggedIn()(MainPageGrid.as_view(http_method_names=['get'])), name='main-grid'),
    path('buypage/', LoggedIn()(PurchaseMainPage.as_view(http_method_names=['get'])), name='buy-page'),
    path('buypage/schecule/', LoggedIn()(PurchaseSchedulePage.as_view(http_method_names=['get'])), name='buy-schedule'),
    path('reviewpage/', LoggedIn()(ReviewPage.as_view(http_method_names=['get'])), name='review-page'),
    path('reviewpage/schedule/', LoggedIn()(ReviewSchedulePage.as_view(http_method_names=['get'])), name='review-schedule'),
    path('folderpage/<int:folder_id>/', LoggedIn()(FolderPage.as_view(http_method_names=['get'])), name='folder-page'),
    path('user/newfolder/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='new-folder'),
        
    path('', LoggedOut()(LogIn.as_view(http_method_names=['get', 'post'])), name='login'),
    path('user/product/count/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='product-count'),
    path('user/product/total/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='total-product'),
    path('user/product/success/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='success-product'),
    path('user/product/fail/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='fail-product'),    
    path('user/product/', LoggedIn()(AboutProduct.as_view(http_method_names=['put', 'post'])), name='product'),
    path('user/product/<int:p_id>/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='product-detail'),
    path('user/product/search/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='search-product'),
    path('user/product/excel/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='product-excel'),
    #TODO
    path('user/product/delete/', AboutProduct.as_view(http_method_names=['delete']), name='products-delete'),
    
    path('user/folder/<int:folder_id>/count/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-detail-count'),
    path('user/folder/<int:folder_id>/product/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-product'),
    path('user/folder/<int:folder_id>/product/delete/<int:p_id>/', LoggedIn()(AboutProduct.as_view(http_method_names=['get'])), name='folder-product-delete'),
    path('user/folder/<int:folder_id>/product/<int:p_id>/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-product-detail'),
    path('user/folder/<int:folder_id>/product/search/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-search-product'),
    path('user/folder/<int:folder_id>/product/delete/', LoggedIn()(AboutFolder.as_view(http_method_names=['delete'])), name='folder-products-delete'),
    path('user/folder/', LoggedIn()(AboutFolder.as_view(http_method_names=['put'])), name='product-assign'),
    #TODO
    path('user/folder/<int:folder_id>/excel/', LoggedIn()(AboutFolder.as_view(http_method_names=['get'])), name='folder-excel'),    
    
    path('user/data/detail/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get'])), name='my-data-detail'),
    path('user/data/update/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['put'])), name='update-info'),
    path('user/ticket/count/', LoggedIn()(RequestUserInfo.as_view(http_method_names=['get'])), name='my-ticket'),    
    
    path('history/reviewticket/request/', LoggedIn()(AboutTicket.as_view(http_method_names=['get'])), name='review-ticket'),
    path('history/purchaseticket/request/', LoggedIn()(AboutTicket.as_view(http_method_names=['get', 'put'])), name='purchase-ticket'),
    path('history/reviewticket/request/count/', LoggedIn()(AboutTicket.as_view(http_method_names=['get'])), name='review-ticket-count'),
    path('history/purchaseticket/request/count/', LoggedIn()(AboutTicket.as_view(http_method_names=['get'])), name='purchase-ticket-count'),
    path('request/review/ticket/', LoggedIn()(AboutTicket.as_view(http_method_names=['post'])), name='review-ticket'),
    path('request/purchase/ticket/', LoggedIn()(AboutTicket.as_view(http_method_names=['post'])), name='purchase-ticket'),
    path('request/review/ticket/delete/', LoggedIn()(AboutTicket.as_view(http_method_names=['delete'])), name='review-ticket'),
    path('request/purchase/ticket/delete/', LoggedIn()(AboutTicket.as_view(http_method_names=['delete'])), name='purchase-ticket'),
    
    path('purchase/count/<str:yr_mon_d>', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='date-count'),
    path('purchase/state/count/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='state-count'),
    path('history/purchase/<str:yr_mon_d>/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='date-purchase'),
    path('history/purchase/<str:yr_mon_d>/info/<str:id>/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='detail'),
    path('purchase/history/total/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='total'),
    path('purchase/history/progress/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='total'),
    path('purchase/history/success/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='total'),
    path('purchase/history/fail/', LoggedIn()(AboutPurchase.as_view(http_method_names=['get'])), name='total'),
    # path('purchase/update/', LoggedIn()(AboutPurchase.as_view(http_method_names=['put'])), name='purchase-update'),
    path('regist/purchase/', LoggedIn()(AboutPurchase.as_view(http_method_names=['post'])), name='purchase'),
    path('delete/purchase/', LoggedIn()(AboutPurchase.as_view(http_method_names=['delete'])), name='delete-purchase'),
        
    path('review/count/<str:yr_mon_d>/',LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='date-count'),
    path('review/state/count/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='state-count'),
    path('history/review/<str:yr_mon_d>/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='date-review'),
    path('history/review/<str:yr_mon_d>/info/<str:id>/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='detail'),
    path('review/history/total/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='total'),
    path('review/history/progress/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='progress'),
    path('review/history/success/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='success'),
    path('review/history/fail/', LoggedIn()(AboutReview.as_view(http_method_names=['get'])), name='fail'),
    # path('review/update/', LoggedIn()(AboutReview.as_view(http_method_names=['put'])), name='review-update'),
    path('registe/review/', LoggedIn()(AboutReview.as_view(http_method_names=['post'])), name='review'),
    path('delete/review/', LoggedIn()(AboutReview.as_view(http_method_names=['delete'])), name='delete-purchase'),
    path('fetch/review/contents', LoggedIn()(Revot.as_view(http_method_names=['post'])), name='revot')
]