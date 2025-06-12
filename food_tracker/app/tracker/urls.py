from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_record_list, name='food_record_list'),
    path('new/', views.create_food_record, name='create_food_record'),
    path('success/', views.record_success, name='record_success'),
    path('edit/<int:pk>/', views.edit_food_record, name='edit_food_record'),
    path('delete/<int:pk>/', views.delete_food_record, name='delete_food_record'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('update-image-order/', views.update_image_order, name='update_image_order'),
    path('calendar/', views.food_calendar_view, name='food_calendar'),
    path('calendar-events/', views.food_calendar_events, name='food_calendar_events'),
    path('weight/add/', views.add_weight_record, name='add_weight'),
    path('weight/list/', views.weight_list, name='weight_list'),

]
