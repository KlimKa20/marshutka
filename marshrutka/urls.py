from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('', include('firstpaige.urls')),
    path('marshrutka/', include('accounts.urls')),
    path('marshrutka/', include('book.urls')),
    path('admin/', admin.site.urls),
    path("news/", include('news.urls')),
    path("book/", include('book.urls')),
    path('news/', include('news.urls')),
]
