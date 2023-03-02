from django.shortcuts import render
from main.models.client import ProductFolder
from main.views.security import ParsedClientView


class BasePage(ParsedClientView): 
    template_name = None
    @ParsedClientView.init_parse
    def get(self, req):        
        context = {}        
        context.update(self._client._user_data)
        context["folders"] = [f._folder_data for f in list(ProductFolder.objects.filter(user=self._client))]
        return render(req, self.template_name, context=context)
    

class MainPage(BasePage):    
    template_name = 'index.html'
    
    @ParsedClientView.init_parse
    def get(self, req, folder_id=None):
        context = {}
        context.update(self._client._user_data)
        context["folders"] = [f._folder_data for f in list(ProductFolder.objects.filter(user=self._client))]
        if req.resolver_match.url_name == 'folder-page':            
            context["folder_name"] = [f['name'] for f in context["folders"] if f['id']==folder_id][0]
        return render(req, self.template_name, context=context)

class MainPageGrid(BasePage):
    template_name = 'index_gridview.html'

class MyPage(BasePage):    
    template_name = 'mypage.html'
    
    
class PurchaseMainPage(BasePage):    
    template_name = 'buy_main.html'
    
class PurchaseSchedulePage(BasePage):    
    template_name = 'buy_schedule.html'    

class ReviewPage(BasePage):
    template_name = 'review_main.html'
    
class ReviewSchedulePage(BasePage):
    template_name = 'review_schedule.html'    
    

