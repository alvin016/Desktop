from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    path('detail/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('birthdays/', views.birthday_list, name='birthday_list'),
    path('calendar/', views.birthday_calendar, name='birthday_calendar'),
    path('customer/<int:customer_id>/activity/add/', views.add_activity, name='add_activity'),
    path('activity/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    path('activity/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),

]
