from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    active = models.IntegerField()
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'category'


class Customer(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256, blank=True, null=True)
    coordinates = models.CharField(max_length=32, blank=True, null=True)
    tel = models.CharField(max_length=32, blank=True, null=True)
    active = models.IntegerField()
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'customer'


class DeliveryStaff(models.Model):
    name = models.CharField(max_length=64)
    active = models.IntegerField()
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'delivery_staff'


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    district = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    tel = models.CharField(max_length=32, blank=True, null=True)
    active = models.IntegerField()
    remark = models.CharField(max_length=256, blank=True, null=True)
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    coordinates = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'restaurant'


class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    remark = models.CharField(max_length=256, blank=True, null=True)
    active = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'product'


class ProductType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    active = models.IntegerField()
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'product_type'


class OrderMaster(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_staff = models.ForeignKey(DeliveryStaff, on_delete=models.CASCADE)
    delivered_date = models.CharField(max_length=32)
    delivered_time = models.CharField(max_length=8)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    food_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'order_master'


class OrderDetail(models.Model):
    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    comment = models.CharField(max_length=256, blank=True, null=True)
    active = models.IntegerField()
    create_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        managed = True
        db_table = 'order_detail'
