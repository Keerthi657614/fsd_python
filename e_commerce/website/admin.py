from django.contrib import admin
from website.models import Product, Review, AuthUser
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(AuthUser)
