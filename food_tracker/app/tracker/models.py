from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class FoodRecord(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', '早餐'),
        ('lunch', '中餐'),
        ('dinner', '晚餐'),
        ('snack', '加餐'),
    ]

    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.get_category_display()}"

class FoodImage(models.Model):
    record = models.ForeignKey(FoodRecord, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/food/')

    def save(self, *args, **kwargs):
        if self.image and not str(self.image.name).endswith(".webp"):
            # 讀入圖片
            img = Image.open(self.image)
            img = img.convert('RGB')  # WebP 不支援透明

            # 建立暫存 buffer
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=85)  # 可調整壓縮品質

            # 產生新檔名
            new_name = os.path.splitext(self.image.name)[0] + '.webp'

            # 用 ContentFile 替換掉原本 image 欄位內容
            self.image.save(new_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

class WeightRecord(models.Model):
    date = models.DateField()
    weight = models.FloatField()
    body_fat = models.FloatField()
    visceral_fat = models.FloatField()
    muscle_rate = models.FloatField()
    bmi = models.FloatField()
    bmr = models.FloatField()
    body_age = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.weight} kg"
