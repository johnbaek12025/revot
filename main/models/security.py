from django.db import models
from django.utils.timezone import now

from main.models.client import User



class ClientInfoBaseModel(models.Model):

    class Meta:
        abstract = True

    ip = models.ForeignKey('main.ClientIp', null=True, default=None, blank=True, on_delete=models.SET_NULL)
    user_agent = models.TextField(null=True, default=None, blank=True)
    birth = models.DateTimeField(default=now)


class LoginSession(ClientInfoBaseModel):

    class Meta:
        ordering = ['-birth']
    value = models.CharField(max_length=200, db_index=True, unique=True)    
    account = models.ForeignKey('main.User', on_delete=models.CASCADE)
    logged_out = models.BooleanField(default=False)
    latest_accessed = models.DateTimeField(default=now)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.latest_accessed = now()
        if getattr(self, 'pk', None) is not None:
            self.save()

    def __str__(self):
        return self.account + ' - ' + self.value
    
    
    
class DangerousAction(ClientInfoBaseModel):

    user = models.ForeignKey('main.User', on_delete=models.CASCADE)
    url = models.TextField(null=True, default=None, blank=True)
    method = models.CharField(max_length=10, null=True, default=None, blank=True)
    message = models.TextField(null=True, default=None, blank=True)

    def __str__(self):
        return str(self.owner) + ';' + self.message