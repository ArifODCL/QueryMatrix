from django.contrib import admin
from inventory.models import *
# Register your models here.

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['id', 'name', 'description']


@admin.register(SupplierModel)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_email', 'contact_phone', 'address', 'website']
    search_fields = ['id', 'name', 'contact_email', 'contact_phone', 'address', 'website']

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'category', 'description','unit_price', 'supplier']
    search_fields = ['id', 'name', 'sku', 'category', 'description', 'unit_price', 'supplier']


@admin.register(WarehouseModel)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'capacity', 'description']
    search_fields = ['id', 'name', 'location', 'capacity', 'description']


@admin.register(StockModel)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'warehouse', 'quantity', 'last_updated']
    search_fields = ['id', 'product', 'warehouse', 'quantity']


@admin.register(StockMovementModel)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['id', 'product__name', 'warehouse__name', 'quantity', 'movement_type', 'date', 'created_by']
    search_fields = ['id', 'product__name', 'warehouse__name', 'quantity', 'movement_type', 'date', 'created_by']


@admin.register(PurchaseOrderModel)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'order_date', 'status', 'total_amount']
    search_fields = ['id', 'supplier', 'order_date', 'status', 'total_amount', 'notes']


@admin.register(PurchaseOrderItemModel)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_order', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['id', 'purchase_order', 'product', 'quantity', 'unit_price', 'total_price']


@admin.register(SalesOrderModel)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'order_number', 'order_date', 'status', 'total_amount']
    search_fields = ['id', 'customer_name', 'order_number', 'order_date', 'status', 'total_amount', 'shipping_address', 'notes']


@admin.register(SalesOrderItemModel)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sales_order', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['id', 'sales_order__order_number', 'product__name', 'quantity', 'unit_price', 'total_price']


@admin.register(ProductReturnModel)
class ProductReturnAdmin(admin.ModelAdmin):
    list_display = ['id', 'sales_order_item', 'purchase_order_item', 'quantity', 'return_type', 'date', 'reason']