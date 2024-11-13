from django.db import models


class ProductCategoryModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class SupplierModel(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"


class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE, related_name="category_products")
    supplier = models.ForeignKey(SupplierModel, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to="product_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class WarehouseModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()  # Maximum stock this warehouse can hold
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


class StockModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(WarehouseModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class StockMovementModel(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    MOVEMENT_TYPES = [
        (IN, 'In'),
        (OUT, 'Out'),
    ]

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_stock_movements")
    warehouse = models.ForeignKey(WarehouseModel, on_delete=models.CASCADE, related_name="warehouse_stock_movements")
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)  # Could link to a User model if needed

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"


class PurchaseOrderModel(models.Model):
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')],
        default='PENDING'
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"PO-{self.order_number}"

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


class PurchaseOrderItemModel(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrderModel, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Purchase Order Item"
        verbose_name_plural = "Purchase Order Items"


class SalesOrderModel(models.Model):
    customer_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('SHIPPED', 'Shipped'), ('CANCELLED', 'Cancelled')],
        default='PENDING'
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"SO-{self.order_number}"

    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"


class SalesOrderItemModel(models.Model):
    sales_order = models.ForeignKey(SalesOrderModel, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Sales Order Item"
        verbose_name_plural = "Sales Order Items"


class ProductReturnModel(models.Model):
    sales_order_item = models.ForeignKey(SalesOrderItemModel, on_delete=models.CASCADE, null=True, blank=True)
    purchase_order_item = models.ForeignKey(PurchaseOrderItemModel, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    return_type = models.CharField(
        max_length=10,
        choices=[('SALE', 'Sale Return'), ('PURCHASE', 'Purchase Return')],
    )
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"Return for {self.quantity} of {self.sales_order_item.product.name if self.sales_order_item else self.purchase_order_item.product.name}"

    class Meta:
        verbose_name = "Product Return"
        verbose_name_plural = "Product Returns"
