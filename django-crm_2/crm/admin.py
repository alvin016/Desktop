from django.contrib import admin
from .models import ProductCategory, Product, Customer, CustomerProductStatus

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(CustomerProductStatus)