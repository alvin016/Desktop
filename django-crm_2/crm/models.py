from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.name}"



class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    CONSTELLATION_CHOICES = [
        ('aries', '牡羊座'),
        ('taurus', '金牛座'),
        ('gemini', '雙子座'),
        ('cancer', '巨蟹座'),
        ('leo', '獅子座'),
        ('virgo', '處女座'),
        ('libra', '天秤座'),
        ('scorpio', '天蠍座'),
        ('sagittarius', '射手座'),
        ('capricorn', '魔羯座'),
        ('aquarius', '水瓶座'),
        ('pisces', '雙魚座'),
    ]   


    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    city = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)
    photo = models.ImageField(upload_to='customer_photos/', blank=True, null=True)
    constellation = models.CharField(
        max_length=20,
        choices=CONSTELLATION_CHOICES,
        blank=True,
        null=True
    )
    birthday_md = models.CharField(
        max_length=5,  # 格式 MM-DD
        blank=True,
        null=True,
        help_text='格式為 MM-DD，例如 06-16'
    )
    
    def __str__(self):
        return self.name


class ProductStatusOption(models.Model):
    name = models.CharField(max_length=50)  # e.g. 自己用、親友用、準備購買

    def __str__(self):
        return self.name



class CustomerProductStatus(models.Model):

    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status_options = models.ManyToManyField(ProductStatusOption, blank=True)
    
    class Meta:
        unique_together = ('customer', 'product')  # ✅ 防止重複資料

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"

    
    
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('call', '📞 電話'),
        ('visit', '🏠 面談'),
        ('email', '📧 Email'),
        ('line', '💬 Line'),
        ('other', '📌 其他'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    date = models.DateField(default=timezone.now)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_type_display()}] {self.customer.name}"

@receiver(post_save, sender=Product)
def create_status_for_all_customers(sender, instance, created, **kwargs):
    if created:
        for customer in Customer.objects.all():
            # 檢查是否已存在，避免重複建立
            exists = CustomerProductStatus.objects.filter(customer=customer, product=instance).exists()
            if not exists:
                CustomerProductStatus.objects.create(customer=customer, product=instance)
                

@receiver(post_save, sender=Customer)
def create_product_status_for_new_customer(sender, instance, created, **kwargs):
    if created:
        for product in Product.objects.all():
            exists = CustomerProductStatus.objects.filter(customer=instance, product=product).exists()
            if not exists:
                CustomerProductStatus.objects.create(customer=instance, product=product)