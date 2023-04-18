from django.shortcuts import render
from main.models.client import ProductFolder
from main.views.security import ParsedClientView


class MainPage(ParsedClientView):    
    template_name = 'index.html'

    @ParsedClientView.init_parse
    def get(self, req):        
        context = {}        
        context.update(self._client._user_data)
        context["folders"] = [f._folder_data for f in list(ProductFolder.objects.filter(user=self._client))]
        if req.resolver_match.url_name == 'main':
            self._client.display_type = 1
            self._client.save()
        elif req.resolver_match.url_name == 'main-grid':
            self._client.display_type = 0
            self._client.save()
        print(f"asdassasad{context}")
        return render(req, self.template_name, context=context)

class MainPageGrid(MainPage):
    template_name = 'index_gridview.html'

class MyPage(MainPage):    
    template_name = 'mypage.html'
    
    
class PurchaseMainPage(MainPage):    
    template_name = 'buy_main.html'
    
class PurchaseSchedulePage(MainPage):    
    template_name = 'buy_schedule.html'    

class ReviewPage(MainPage):
    template_name = 'review_main.html'
    
class ReviewSchedulePage(MainPage):
    template_name = 'review_schedule.html'    
    
class FolderPage(ParsedClientView):
    template_name = 'folder_detail.html'

    @ParsedClientView.init_parse
    def get(self, req, folder_id=None):
        context = {}
        context.update(self._client._user_data)
        context["folders"] = [f._folder_data for f in list(ProductFolder.objects.filter(user=self._client))]        
        context["folder_name"] = [f['name'] for f in context["folders"] if f['id']==folder_id][0]            
        return render(req, self.template_name, context=context)