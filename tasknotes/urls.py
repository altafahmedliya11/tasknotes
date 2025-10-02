from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),

    # include app-level urls
    path('api/', include('employees.urls')),  
]
