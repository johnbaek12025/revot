from django.db import models
from django.utils.timezone import now
# Create your models here.

class Worker(models.Model):
    pass

class WorkLog(models.Model):
    pass


class NAccount(models.Model):
    nid = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    purchased = models.ForeignKey('main.Purchase', on_delete=models.CASCADE)
    reviewed = models.ForeignKey('main.Review', on_delete=models.CASCADE)
    birth = models.DateTimeField(default=now)
    
class Ip(models.Model):

    worker = models.ManyToManyField('Worker', blank=True)  # 실제로는 사용하고 있지 않음. traffic log 통해서 worker 조회
    memo = models.TextField(null=True, default=None, blank=True)
    address = models.CharField(max_length=15, unique=True, db_index=True)
    birth = models.DateTimeField(default=now)