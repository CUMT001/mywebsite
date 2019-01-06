from django.contrib import admin
from django.urls import path, include
from . import views
from my_app.views import article_detail,article_list
from django.conf import settings
from django.conf.urls.static import static

# 规定哪些网址有效
urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
]
