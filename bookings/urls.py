from django.urls import path
from .views import booking_list, create_booking

urlpatterns = [
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/create/', create_booking, name='create_booking'),
]