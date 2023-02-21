from django.contrib import admin

from main.models import client, clientdata, pseudo, security


admin.site.register([
    client.User, client.Product, client.State, client.ProductFolder, clientdata.RequestTicket,
    client.ClientIp, pseudo.Purchase, pseudo.Review
                     ])