from django.urls import path

from manager.views import TicketManage, UserManage, ManageIp
from main.views.security import LoggedIn


app_name = 'devoperator'

urlpatterns = [
    path('user/', LoggedIn([1, 2])(UserManage.as_view(http_method_names=['get'])), name='user-data'), 
    path('user/auth/', LoggedIn([1, 2])(UserManage.as_view(http_method_names=['put'])), name='authorization'),     
    path('check/review/ticket/', LoggedIn([2], True)(TicketManage.as_view(http_method_names=['get', 'put'])), name='review-ticket'),
    path('check/purchase/ticket/', LoggedIn([2], True)(TicketManage.as_view(http_method_names=['get', 'put'])), name='purchase-ticket'),
    path('check/review/ticket/count/', LoggedIn([2], True)(TicketManage.as_view(http_method_names=['get'])), name='review-ticket-count'),
    path('check/purchase/ticket/count/', LoggedIn([2], True)(TicketManage.as_view(http_method_names=['get'])), name='purchase-ticket-count'),
    path('ticket/reject/', LoggedIn([2], True)(TicketManage.as_view(http_method_names=['put'])), name='reject-ticket-request'),
    # path('ip/'LoggedIn([2], True)(ManageIp.as_view(http_method_names=['get', 'post'])), name='ip-assign'),
]