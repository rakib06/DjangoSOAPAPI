
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from customer.views import  CustomerService

urlpatterns = [
    path('admin/', admin.site.urls),
    
    url(r'^customer/', DjangoView.as_view(
        services=[CustomerService], tns='spyne.examples.customer',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    
]
