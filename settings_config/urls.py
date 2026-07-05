from django.urls import path
from .views import crm_settings

urlpatterns = [
    path(
        'settings/',
        crm_settings,
        name='crm_settings'
    ),
]