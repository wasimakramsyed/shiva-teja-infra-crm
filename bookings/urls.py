from django.urls import path
from .views import (
    booking_list,
    create_booking,
    booking_profile,
    edit_booking,
    print_booking,
    load_plots
)

urlpatterns = [

    path(
        'bookings/',
        booking_list,
        name='booking_list'
    ),

    path(
        'bookings/create/',
        create_booking,
        name='create_booking'
    ),

    path(
        'ajax/load-plots/',
        load_plots,
        name='ajax_load_plots'
    ),

    path(
        'bookings/<int:booking_id>/',
        booking_profile,
        name='booking_profile'
    ),

    path(
        'bookings/edit/<int:booking_id>/',
        edit_booking,
        name='edit_booking'
    ),

    path(
        'bookings/print/<int:booking_id>/',
        print_booking,
        name='print_booking'
    ),

]