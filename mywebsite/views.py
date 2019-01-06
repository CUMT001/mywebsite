from django.shortcuts import render_to_response, redirect, render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7_days_hot_data
from my_app.models import Article
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User

def get_7_days_hot_blogs():
	today = timezone.now().date()
	date = today-datetime.timedelta(days=7)
	blogs = Article.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values('id','title').annotate(Sum('read_details__read_num')).order_by('-read_details__read_num__sum')
	return blogs

def index(request):
	blog_content_type = ContentType.objects.get_for_model(Article)
	dates,read_nums = get_seven_days_read_data(blog_content_type)
	today_hot_data = get_today_hot_data(blog_content_type)
	yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
	week_hot_data = cache.get('week_hot_data')
	if week_hot_data is None:
		week_hot_data = get_7_days_hot_blogs()
		cache.set('week_hot_data', week_hot_data, 60*60)
	context={}
	context['dates'] = dates
	context['read_nums'] = read_nums
	context['today_hot_data'] = today_hot_data
	#想加昨天热门博客直接改前端页面
	context['yesterday_hot_data'] = yesterday_hot_data
	context['week_hot_data'] = week_hot_data
	return render(request, "init.html",context)
	
def login(request):
	if request.method=='POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request,user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		login_form = LoginForm()
	context = {}
	context['login_form'] = login_form
	return render(request, 'login.html', context)
	
def register(request):
	if request.method=='POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']
			user = User.objects.create_user(username, email, password)
			user.save()
			user = auth.authenticate(username=username,password=password)
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		reg_form = RegForm()
	context = {}
	context['reg_form'] = reg_form
	return render(request, 'register.html', context)