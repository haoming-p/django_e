from django.db import models

# Create your models here.
# django会自动对每个class设置id作为primary_key, 可以将某一个字段(primary_key=True), django就不会对该字段生成id并用作primary key
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # circular relationships, 使用'Product'而不是Product, 但如果统一改变量名, 'Product'中的不会被改到
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') # 因为Product中已经有一个collection, 所以要改名

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Product(models.Model):
    # https://docs.djangoproject.com/en/5.1/ref/models/fields/
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True)   # url中的the-ultimate-django-part1-1, 帮助搜索
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)           # 自动更新
    # 与collection, collection一对多
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)    # delete collection, 不会删除product
    # 与Promotion，多对多
    promotions = models.ManyToManyField(Promotion) 

class Customer(models.Model):
    MEMBERSHIP_Bronze = 'B' 
    MEMBERSHIP_Silver = 'S'
    MEMBERSHIP_Gold = 'G'

    MEMBERSHIP_CHOICES = [  # 大写表示fixed list of values
        (MEMBERSHIP_Bronze, 'Bronze'),
        (MEMBERSHIP_Silver, 'Silver'),
        (MEMBERSHIP_Gold, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)          # 唯一
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)        # nullable
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_Bronze)  # 从list中选择，设置默认

    class Meta: # customize database schema
        db_table= 'store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # 与Customer, Customer一对多
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # 与Customer, Customer一对一，不需要对Customer额外处理
    # customor = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True)  
    # 与Customer, Customer一对多
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) # delete Customer时delete Address
    

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()