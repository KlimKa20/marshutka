from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.views.generic import ListView, DetailView
from news.models import Articles

urlpatterns = [
    re_path(r'^$', ListView.as_view(queryset=Articles.objects.all()[:20],
                                    template_name="news/postu.html")),
    re_path(r'^(?P<pk>\d+)$', DetailView.as_view(model=Articles, template_name="news/post.html"))
]
