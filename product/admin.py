from django.contrib import admin

from product.models import Product, Like, Favorites, ProductImages

# Register your models here.
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Favorites)
admin.site.register(ProductImages)
