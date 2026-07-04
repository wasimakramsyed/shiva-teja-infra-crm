from django.urls import path
from .views import (
    dashboard_home,
    sales_dashboard,
    accounts_dashboard
)

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('sales-dashboard/', sales_dashboard, name='sales_dashboard'),
    path('accounts-dashboard/', accounts_dashboard, name='accounts_dashboard'),
]