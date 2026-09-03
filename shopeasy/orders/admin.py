from django.contrib import admin
from .models import Coupon, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price_at_purchase', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'subtotal', 'discount_amount', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'shipping_city', 'shipping_pincode')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'valid_from', 'valid_to', 'usage_limit', 'times_used')
    list_filter = ('active',)
    search_fields = ('code',)
