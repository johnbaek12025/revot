import json
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

    
    
class ClientIp(models.Model):
    ip_address = models.CharField(max_length=20, unique=True, db_index=True)


class User(models.Model):    
    class Meta:    
        ordering = ['-birth']        
    is_operator = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=22, null=True, default=None, blank=True)
    email_account = models.CharField(max_length=100, null=True, blank=True, default=None)
    password = models.CharField(max_length=200)    
    agency_code = models.CharField(max_length=6, null=True, blank=True, default=None)
    recommendation_code = models.CharField(max_length=20, null=True, blank=True, default=None)    
    self_code = models.CharField(max_length=20, null=True, blank=True, default=None)
    
    authorization = models.BooleanField(default=False)
    authorized_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    allowed_ip = models.ManyToManyField('main.ClientIp', blank=True)
    purchase_ticket = models.PositiveIntegerField(default=0)
    review_ticket = models.PositiveIntegerField(default=0)
    birth = models.DateTimeField(default=now)
    remember_account = models.BooleanField(default=False)
    display_type = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    higherarchy = models.ForeignKey('main.State', on_delete=models.CASCADE)
    
    @property
    def _user_data(self):
        if self.higherarchy == 0:
            return {"id": self.id ,"auth": self.authorization, "name": self.name, "phone":self.phone, "product_ticket": self.purchase_ticket, "review_ticket": self.purchase_ticket, "agency_code": self.agency_code, "recommendation_code": self.recommendation_code, "manager_name": self.authorized_by.name, "manager_phone": self.authorized_by.phone, "self_code": self.self_code}
        return {"id": self.id ,"auth": self.authorization, "name": self.name, "phone":self.phone, "product_ticket": self.purchase_ticket, "review_ticket": self.purchase_ticket, "agency_code": self.agency_code, "recommendation_code": self.recommendation_code, "self_code": self.self_code}
        
    @property
    def _user_data_detail(self):
        return {"name": self.name, "phone": self.phone, "account": self.email_account, "agency_code": self.agency_code, "recommendation_code": self.recommendation_code, "self_code": self.self_code}
        
    
    @property
    def _user_tickets(self):
        return {"review_ticket": self.review_ticket, "purchase_ticket": self.purchase_ticket}

class Product(models.Model):    
    class Meta:    
        ordering = ['-birth']
    birth = models.DateTimeField(default=now)
    owner = models.ForeignKey('main.User', on_delete=models.CASCADE)
    folder = models.ForeignKey('main.ProductFolder', on_delete=models.SET_NULL, null=True)
    mid1 = models.CharField(max_length=255, null=True, blank=True, default=None)
    mid2 = models.CharField(max_length=255, null=True, blank=True, default=None)
    pid = models.CharField(max_length=255, null=True, blank=True, default=None)
    mall_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    img_url = models.CharField(max_length=255, null=True, blank=True, default=None)
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    keyword = models.TextField()
    state = models.ForeignKey('main.State', on_delete=models.CASCADE)
    searching_type = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    options = models.TextField()
    price = models.CharField(max_length=100, null=True, blank=True, default=None)
    
    def save(self, *args, **kwargs):
        # Convert the dictionary to a JSON string and store it in the field
        self.options = json.dumps(self.options, ensure_ascii=False)
        super().save(*args, **kwargs)    
    
    
    @property
    def _product_data(self):
        return {"id": self.id, "pid": self.pid, "mid1": self.mid1, "keyword": self.keyword}


class ProductFolder(models.Model):
    class Meta:    
        ordering = ['-birth']
    birth = models.DateTimeField(default=now)
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)    
    
    @property
    def _folder_data(self):
        return {"id": self.id, "name": self.name, "product_count": self.product_set.count()}
    
    @classmethod
    def get_next_folder_name(cls):
        last_folder = cls.objects.order_by('-name').first()
        if last_folder:
            last_folder_number = int(last_folder.name.split('폴더')[-1])
        else:
            last_folder_number = 0
        return f"폴더{last_folder_number + 1}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_next_folder_name()
        super().save(*args, **kwargs)
    
    
    
class State(models.Model):
    state = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], default=0, verbose_name='state')