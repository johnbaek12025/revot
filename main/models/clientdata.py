from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

class RequestTicket(models.Model):
    class Meta:    
        ordering = ['-id']
    user = models.ForeignKey('main.User', on_delete=models.CASCADE)
    bank = models.CharField(max_length=10)
    ticket_type = models.CharField(max_length=100)
    depositor_name = models.CharField(max_length=20)
    state = models.ForeignKey('main.State', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    birth = models.DateTimeField(default=now)

    @property
    def _request_state(self):        
        return {
                    "id": self.id, 
                    "type": self.ticket_type, 
                    "count": self.count, 
                    "depositor_name": self.depositor_name, 
                    "bank":self.bank, 
                    "state": self.state.state,
                    # "higherarchy": self.user.higherarchy.state,
                    "account": self.user.email_account,
                    "r_date": self.birth.strftime('%y-%m-%d')
                }
                