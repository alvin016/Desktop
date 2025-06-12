from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer,Activity
from .forms import CustomerForm,ActivityForm
import calendar
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_form.html', {'form': form, 'title': '新增客戶'})

@permission_required('crm.change_customer', raise_exception=True)
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_form.html', {'form': form, 'title': '編輯客戶'})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'crm/customer_confirm_delete.html', {'customer': customer})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'crm/customer_detail.html', {'customer': customer})

@login_required
def birthday_list(request):
    today = datetime.today()
    this_month = f"{today.month:02d}"  # e.g. "06"

    # 篩選 birthday_md 以 "06-" 開頭者
    customers = Customer.objects.filter(birthday_md__startswith=this_month)
    return render(request, 'crm/birthday_list.html', {
        'customers': customers,
        'month': this_month,
    })

@login_required
def customer_list(request):
    keyword = request.GET.get("q", "")
    constellation = request.GET.get("constellation", "")
    city = request.GET.get("city", "")

    customer_list = Customer.objects.all()

    if keyword:
        customer_list = customer_list.filter(
            Q(name__icontains=keyword) |
            Q(email__icontains=keyword) |
            Q(phone__icontains=keyword)
        )

    if constellation:
        customer_list = customer_list.filter(constellation=constellation)

    if city:
        customer_list = customer_list.filter(city=city)

    paginator = Paginator(customer_list, 10)
    page_number = request.GET.get("page")
    customers = paginator.get_page(page_number)

    # 用於下拉選單選項
    city_list = Customer.objects.values_list('city', flat=True).distinct().order_by('city')
    constellation_list = Customer.CONSTELLATION_CHOICES

    return render(request, 'crm/customer_list.html', {
        'customers': customers,
        'keyword': keyword,
        'constellation': constellation,
        'city': city,
        'city_list': city_list,
        'constellation_list': constellation_list,
    })

@login_required    
def birthday_calendar(request):
    # 取得目前月份
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 取出所有生日在這個月的客戶
    all_birthdays = []
    for c in Customer.objects.exclude(birthday_md__isnull=True):
        try:
            month_day = datetime.strptime(c.birthday_md, "%m-%d")
            if month_day.month == month:
                all_birthdays.append({
                    "name": c.name,
                    "date": f"{year}-{month_day.month:02d}-{month_day.day:02d}",
                    "id": c.id,
                })
        except:
            pass  # 若格式錯誤忽略

    context = {
        'year': year,
        'month': month,
        'birthdays': all_birthdays,
    }
    return render(request, 'crm/birthday_calendar.html', context)


@login_required
def add_activity(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.customer = customer
            activity.created_by = request.user
            activity.save()
            return redirect('customer_detail', customer_id)
    else:
        form = ActivityForm()
    return render(request, 'crm/add_activity.html', {'form': form, 'customer': customer})

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    customer_id = activity.customer.id
    if request.user == activity.created_by or request.user.is_superuser:
        activity.delete()
    return redirect('customer_detail', customer_id)

# views.py
@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.user != activity.created_by and not request.user.is_superuser:
        return redirect('customer_detail', activity.customer.id)

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', activity.customer.id)
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'crm/edit_activity.html', {'form': form, 'activity': activity})
