from django.contrib import admin
from django.urls import path
from . import views
from .views import article_detail,article_list

# 规定哪些网址有效
urlpatterns = [
	path('', article_list, name="list"),
	path('<int:article_id>', article_detail, name="article_de"),
	path('type/<int:blogs_with_type>', views.article_with_type, name="article_with_type"),
	path('date/<int:year>/<int:month>', views.article_with_date, name="article_with_date")
]