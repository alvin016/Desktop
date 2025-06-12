from django.shortcuts import render, redirect, get_object_or_404
from .forms import FoodRecordForm,WeightRecordForm
from .models import FoodImage,FoodRecord,WeightRecord
from django.http import HttpResponseForbidden,JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


@csrf_exempt
def create_food_record(request):
    if request.method == 'POST':
        form = FoodRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            images = request.FILES.getlist('images')
            for i, image in enumerate(images[:3]):  # 最多3張
                FoodImage.objects.create(record=record, image=image)
            return redirect('record_success')
    else:
        form = FoodRecordForm()
    return render(request, 'tracker/create_record.html', {'record_form': form})            

def record_success(request):
    return render(request, 'tracker/record_success.html')

def food_record_list(request):
    records = FoodRecord.objects.prefetch_related('images').order_by('-date')
    

    # 取得篩選參數
    category = request.GET.get('category')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    # 濾掉空值
    filters = Q()
    if category:
        filters &= Q(category=category)
    if start_date:
        filters &= Q(date__gte=start_date)
    if end_date:
        filters &= Q(date__lte=end_date)

    records = records.filter(filters)
    
    paginator = Paginator(records, 6)  # 每頁6筆
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/record_list.html', {
        'page_obj': page_obj,
        'records': records,
        'selected_category': category,
        'start_date': start_date,
        'end_date': end_date,
    })
    
@csrf_exempt
def edit_food_record(request, pk):
    record = get_object_or_404(FoodRecord, pk=pk)
    remain = 3 - record.images.count()  # ✅ 加入這行

    if request.method == 'POST':
        form = FoodRecordForm(request.POST, instance=record)
        new_images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()
            for img in new_images[:remain]:
                FoodImage.objects.create(record=record, image=img)
            return redirect('food_record_list')
    else:
        form = FoodRecordForm(instance=record)

    return render(request, 'tracker/edit_record.html', {
        'record_form': form,
        'record': record,
        'remain': remain  # ✅ 確保這個變數有傳入 template
    })

@csrf_exempt
def delete_food_record(request, pk):
    record = get_object_or_404(FoodRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('food_record_list')
    return render(request, 'tracker/confirm_delete.html', {'record': record})

@csrf_exempt
def update_image_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for index, img_id in enumerate(data.get('order', [])):
                FoodImage.objects.filter(id=img_id).update(sort_order=index)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

@csrf_exempt
def delete_image(request, image_id):
    image = get_object_or_404(FoodImage, pk=image_id)
    if request.method == 'POST':
        record_pk = image.record.pk
        image.delete()
        return redirect('edit_food_record', pk=record_pk)
    return HttpResponseForbidden("不允許的請求")

def food_calendar_view(request):
    return render(request, 'tracker/calendar.html')

def food_calendar_events(request):
    records = FoodRecord.objects.all()
    category_colors = {
        'breakfast': '#FFDD57',
        'lunch': '#42A5F5',
        'dinner': '#66BB6A',
        'snack': '#EF5350',
    }
    events = [] 
    for record in records:
        events.append({
            'title': record.get_category_display(),
            'start': str(record.date),
            'url': f"/edit/{record.id}/",
            'color': category_colors.get(record.category, '#999')  # 預設灰色
        })
    return JsonResponse(events, safe=False)


def add_weight_record(request):
    if request.method == 'POST':
        form = WeightRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('weight_list')
    else:
        form = WeightRecordForm()
    return render(request, 'tracker/add_weight.html', {'form': form})

def weight_list(request):
    records = WeightRecord.objects.order_by('date')
    
    chart_labels = [str(r.date) for r in records]
    weights = [r.weight for r in records]
    body_fats = [r.body_fat for r in records]

    return render(request, 'tracker/weight_list.html', {
        'records': records,
        'labels': chart_labels,
        'weights': weights,
        'body_fats': body_fats,
    })


def fix_image_orientation(image_field):
    try:
        image = Image.open(image_field)
        image = image.convert('RGB')  # 加上防錯轉換
        exif = image._getexif()
        if exif:
            orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None)
            if orientation_key:
                orientation = exif.get(orientation_key)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)

        image_io = BytesIO()
        image.save(image_io, format='WEBP', quality=85)
        image_io.seek(0)

        return InMemoryUploadedFile(
            image_io, None, image_field.name, 'image/webp',
            image_io.getbuffer().nbytes, None
        )
    except Exception as e:
        print("圖片處理失敗:", e)
        return image_field

