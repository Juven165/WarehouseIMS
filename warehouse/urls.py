from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('suppliers/', include('suppliers.urls')),
    path('accounts/', include('accounts.urls')),
    path('staff/', include('staff.urls')),
]