from django.contrib import admin
from .models import product, cart


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["category", "title", "price"]

@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["product_id", "user_id", "product_quentity"]
