from django.contrib import admin
from django.urls import path, include
from tasknotes.views import SearchAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/search/", SearchAPIView.as_view(), name="search"),
    # include app-level urls
    path("api/", include("employees.urls")),  # Employee & Task APIs
    path("api/", include("notes.urls")),  # Notes & Tags APIs
]
