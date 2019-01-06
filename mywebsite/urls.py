"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from my_app.views import article_detail,article_list
from django.conf import settings
from django.conf.urls.static import static

# 规定哪些网址有效
urlpatterns = [
    path('admin/', admin.site.urls),
	# 空字符串表示只要打开网站就是这个网页,使用views.index处理请求
	path('',views.index, name='home'),
	path('ckeditor', include('ckeditor_uploader.urls')),
	path('article/', include('my_app.urls')),
	path('login/', views.login, name="login"),
	path('register/', views.register, name="register"),
	path('comment/',include('comment.urls'))
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)