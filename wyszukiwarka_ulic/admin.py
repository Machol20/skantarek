from django.contrib import admin
from .models import Street, Building, Sell, ForSale, Salesman, Offer, StreetOffer

admin.site.register(Street)
admin.site.register(Building)
admin.site.register(Sell)
admin.site.register(ForSale)
admin.site.register(Salesman)
admin.site.register(Offer)
admin.site.register(StreetOffer)
