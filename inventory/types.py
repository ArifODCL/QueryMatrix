from graphene_django import DjangoObjectType
from inventory.models import *


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategoryModel
        name = "ProductCategoryModel"
        fields = "__all__"



class SupplierType(DjangoObjectType):
    class Meta:
        model = SupplierModel
        name = "SupplierModel"
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = ProductModel
        name = "ProductModel"
        fields = "__all__"


class WarehouseType(DjangoObjectType):
    class Meta:
        model = WarehouseModel
        name = "WarehouseModel"
        fields = "__all__"


class StockType(DjangoObjectType):
    class Meta:
        model = StockModel
        name = "StockModel"
        fields = "__all__"


class StockMovementType(DjangoObjectType):
    class Meta:
        model = StockMovementModel
        name = "StockMovementModel"
        fields = "__all__"


class PurchaseOrderType(DjangoObjectType):
    class Meta:
        model = PurchaseOrderModel
        name = "PurchaseOrderModel"
        fields = "__all__"


class PurchaseOrderItemType(DjangoObjectType):
    class Meta:
        model = PurchaseOrderItemModel
        name = "PurchaseOrderItemModel"
        fields = "__all__"


class SalesOrderType(DjangoObjectType):
    class Meta:
        model = SalesOrderModel
        name = "SalesOrderModel"
        fields = "__all__"

    
class SalesOrderItemType(DjangoObjectType):
    class Meta:
        model = SalesOrderItemModel
        name = "SalesOrderItemModel"
        fields = "__all__"


class ProductReturnType(DjangoObjectType):
    class Meta:
        model = ProductReturnModel
        name = "ProductReturnModel"
        fields = "__all__"
