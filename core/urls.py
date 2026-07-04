from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('', include('accounts.urls')),
    path('', include('employees.urls')),
    path('', include('teams.urls')),
    path('', include('leads.urls')),
    path('', include('customers.urls')),
    path('', include('bookings.urls')),
    path('', include('payments.urls')),
    path('', include('registrations.urls')),
    path('', include('reports.urls')),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) 