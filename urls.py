from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('report/', include('core.urls')),
    path('admina/', admin.site.urls),
]
