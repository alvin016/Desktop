from django.contrib import admin
from .models import FoodRecord, FoodImage,WeightRecord

class FoodImageInline(admin.TabularInline):
    model = FoodImage
    extra = 3
    max_num = 3

class FoodRecordAdmin(admin.ModelAdmin):
    inlines = [FoodImageInline]
    list_display = ['date', 'category', 'note']

admin.site.register(FoodRecord, FoodRecordAdmin)


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'weight', 'body_fat', 'visceral_fat', 'muscle_rate', 'bmi', 'bmr', 'body_age']