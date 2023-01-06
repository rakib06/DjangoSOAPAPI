from spyne import Mandatory as M
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
from spyne.server.django import DjangoApplication
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne import Array, Iterable, ComplexModel
from spyne import Application, rpc, ServiceBase, Integer, Unicode
import logging
logging.basicConfig(level=logging.DEBUG)


class customer(ComplexModel):
    # user_name = Unicode(64, pattern='[a-z0-9_-]')
    # email_address = Unicode(128, pattern='[^@]+@[^@]+')
    ID = M(Integer, type_name='ID')
    Name = M(Unicode, type_name='Name')
    Email = M(Unicode, type_name='Email')
    Phone = M(Unicode, type_name='Phone')


# CustomersArray = M(customerID)


class CustomerService(ServiceBase):

    @rpc(Unicode, Unicode, Unicode,  _returns=[Unicode, Unicode], _out_variable_names=["Status", "ID"])
    def create(ctx, Name, Email, Phone):
        new_customer = Customer(Name=Name, Email=Email, Phone=Phone, )

        try:
            new_customer.save()
            ID = new_customer.ID

        except Exception as e:
            # return ["Failed", 'email already in use' ]
            return ["Creation Failed", str(e)]
        return ["Created", ID]

    # _out_variable_names=Array[["ID", "Name", "Email", "Phone"]

    @rpc(_returns=Iterable(customer), _out_variable_name='customers')
    def getall(ctx):

        all_customers = Customer.objects.all()
        all_customers_array = []
        for item in all_customers:
            all_customers_array.append(
                [item.ID, item.Name, item.Email, item.Phone])
        return all_customers_array

    @ rpc(Integer, _returns=(customer), _out_variable_name="customer")
    def get_by_id(ctx, ID):
        customer = Customer.objects.get(ID=ID)

        return [customer.ID, customer.Name, customer.Email, customer.Phone]


application = Application([CustomerService],
                          tns='spyne.examples.customer',
                          in_protocol=HttpRpc(validator='soft'),

                          out_protocol=Soap11()
                          )


hello_app = csrf_exempt(DjangoApplication(application))
