from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Activity, ProductStatusOption, ProductCategory, Product,CustomerProductStatus
from .forms import CustomerForm, ActivityForm,CustomerProductStatusForm
import calendar
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect

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

@login_required
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
    category_id = request.GET.get('category')  # ✅ 取得篩選分類

    FormSet = modelformset_factory(CustomerProductStatus, form=CustomerProductStatusForm, extra=0)

    qs = CustomerProductStatus.objects.filter(customer=customer).select_related("product__category")

    if category_id:
        qs = qs.filter(product__category_id=category_id)

    if request.method == 'POST':
        formset = FormSet(request.POST, queryset=qs)
        if formset.is_valid():
            formset.save()
            return redirect('customer_detail', pk)
    else:
         formset = FormSet(queryset=qs)

    category_list = ProductCategory.objects.all()

    return render(request, 'crm/customer_detail.html', {
        'customer': customer,
        'product_status_forms': formset,
        'category_list': category_list,
        'selected_category_id': int(category_id) if category_id else None,
    })

    
@login_required
def birthday_list(request):
    today = datetime.today()
    this_month = f"{today.month:02d}"
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
    product_id = request.GET.get("product", "")
    product_status = request.GET.get("product_status", "")
    
    customer_list = Customer.objects.all().order_by('id')

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

    if product_id and product_status:
        customer_ids = CustomerProductStatus.objects.filter(
            product_id=product_id,
            status_options__id=product_status
        ).values_list("customer_id", flat=True).distinct()
        
        customer_list = customer_list.filter(id__in=customer_ids)

    paginator = Paginator(customer_list, 10)
    page_number = request.GET.get("page")
    customers = paginator.get_page(page_number)

    city_list = Customer.objects.values_list('city', flat=True).distinct().order_by('city')
    constellation_list = Customer.CONSTELLATION_CHOICES
    hightech_products = Product.objects.filter(category__name="高科技")
    product_status_choices = ProductStatusOption.objects.all()

    return render(request, 'crm/customer_list.html', {
        'customers': customers,
        'keyword': keyword,
        'constellation': constellation,
        'city': city,
        'city_list': city_list,
        'constellation_list': constellation_list,
        "product": product_id,
        "product_status": product_status,
        "product_list": hightech_products,
        "product_status_choices": product_status_choices,
    })


@login_required
@login_required
def birthday_calendar(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 處理跨年月份錯誤
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    birthdays = []
    customers = Customer.objects.exclude(birthday_md__isnull=True)

    for c in customers:
        try:
            # 將生日轉為該年格式
            month_day = datetime.strptime(c.birthday_md, "%m-%d")
            birthday_this_year = date(year, month_day.month, month_day.day)

            birthdays.append({
                "name": c.name,
                "date": birthday_this_year.isoformat(),  # e.g. 2025-08-16
                "id": c.id,
            })
        except Exception:
            continue

    return render(request, 'crm/birthday_calendar.html', {
        'year': year,
        'month': month,
        'birthdays': birthdays,
    })


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

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    customer_id = activity.customer.id
    if request.user == activity.created_by or request.user.is_superuser:
        activity.delete()
    return redirect('customer_detail', customer_id)


@login_required
def fix_missing_customer_product_status(request):
    created_count = 0
    for customer in Customer.objects.all():
        for product in Product.objects.all():
            if not CustomerProductStatus.objects.filter(customer=customer, product=product).exists():
                CustomerProductStatus.objects.create(customer=customer, product=product)
                created_count += 1

    messages.success(request, f"✅ 補齊 {created_count} 筆缺漏資料")
    return redirect('customer_list')
