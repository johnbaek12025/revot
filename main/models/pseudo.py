from django.db import models
from django.utils.timezone import now


class Purchase(models.Model):
    class Meta:    
        ordering = ['-reservation_date']
    def today_date():
        return str(now().date())
    birth = models.DateTimeField(default=now)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    reservation_date = models.CharField(default=today_date, db_index=True, max_length=8)
    reservation_at = models.CharField(max_length=8, db_index=True, null=True)
    done = models.CharField(max_length=8, db_index=True, null=True)
    state = models.ForeignKey('main.State', on_delete=models.CASCADE)    
          


class Review(models.Model):
    class Meta:    
        ordering = ['-reservation_date']
    def today_date():
        return str(now().date())
    birth = models.DateTimeField(default=now)
    purchase = models.ForeignKey('main.Purchase', on_delete=models.CASCADE)
    reservation_date = models.CharField(default=today_date, db_index=True, max_length=8)
    reservation_at = models.CharField(max_length=8, db_index=True, null=True)
    done = models.CharField(max_length=8, db_index=True, null=True)
    contents = models.TextField(null=True, blank=True)
    auto_fill = models.BooleanField(default=False)
    state = models.ForeignKey('main.State', on_delete=models.CASCADE)
    img = models.ForeignKey('main.Image', on_delete=models.CASCADE, null=True)
    

class Image(models.Model):
    class Meta:    
        ordering = ['-birth']
    birth = models.DateTimeField(default=now)        
    img = models.ImageField(upload_to='review/pictures/%Y/%m/%d/', blank=True)
    