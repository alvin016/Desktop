from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

PRODUCT_CHOICES = [
    ('y', '用'),
    ('n', '聽'),
    ('z', '說'),
    ('na','無')
]


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('call', '📞 電話'),
        ('visit', '🏠 面談'),
        ('email', '📧 Email'),
        ('line', '💬 Line'),
        ('other', '📌 其他'),
    ]

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
    detergent_status = models.CharField("濃縮洗碗精", max_length=10, choices=PRODUCT_CHOICES, default='na')
    loc_status = models.CharField("L.O.C.", max_length=10, choices=PRODUCT_CHOICES, default='na')
    sa8_status = models.CharField("SA8", max_length=10, choices=PRODUCT_CHOICES, default='na')

    def __str__(self):
        return self.name

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