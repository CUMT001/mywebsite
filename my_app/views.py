from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from .models import Article, ArticleType
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
def article_detail(request, article_id):
	try:
		article = Article.objects.get(id=article_id)
		read_cookie_key = read_statistics_once_read(request, article)
		blog_dates = Article.objects.dates('create_time', 'month', order='DESC')
		all_type = ArticleType.objects.all()
		type_list = []
		for type in all_type:
			type.article_with_type_cnt = Article.objects.filter(article_type=type).count()
			type_list.append(type)
		"""
			获取某个类别数量的简单方法
			article_type.objects.annotate(blog_cnt=Count('article'))
		"""
		blog_dates_dict = {}
		for blog_date in blog_dates:
			blog_cnt = Article.objects.filter(create_time__year = blog_date.year, create_time__month = blog_date.month).count()
			blog_dates_dict[blog_date] = blog_cnt
		blog_content_type = ContentType.objects.get_for_model(article)
		comments = Comment.objects.filter(content_type=blog_content_type,object_id=article.id,parent=None)
		context = {}
		context["article_obj"] = article
		context["previous_blog"] = Article.objects.filter(create_time__gt=article.create_time).last()
		context["next_blog"] = Article.objects.filter(create_time__lt=article.create_time).first()
		context["article_dates"] = blog_dates_dict
		context["article_type"] = type_list
		context["comments"] = comments
		context["comment_form"] = CommentForm(initial={'content_type':blog_content_type.model, 'object_id':article_id, 'reply_comment_id': '0'})
		response = render(request, "article_detail.html", context)
		response.set_cookie('blog_%s_read' %article_id, 'true', max_age=60)
		return response
	except Article.DoesNotExist:
		raise Http404("没有更多文章啦！")
	# return HttpResponse("文章标题：%s<br>文章内容: %s" %(article.title, article.content))
	
def article_list(request):
	#获取页码
	page_num=request.GET.get('page',1)
	articles = Article.objects.filter(is_deleted=False)
	paginator = Paginator(articles,10)
	page_of_blogs = paginator.get_page(page_num)
	current_page = page_of_blogs.number
	display_num = range(max(current_page-3, 1), min(current_page+4, paginator.page_range[-1]+1))
	context={}
	#当前页所有的文章
	context['blogs'] = page_of_blogs.object_list
	#当前页
	context['this_page'] = page_of_blogs
	#分页器
	context['blog_page'] = paginator
	#所有文章
	context['article_list'] = articles
	#显示的页面数
	context['page_range'] = display_num
	return render(request, "article_list.html", context)
	
def article_with_type(request, blogs_with_type):
	content ={}
	try:
		type = ArticleType.objects.filter(id = blogs_with_type)[0]
	except ArticleType.DoesNotExist:
		raise Http404("没有这种博客类型哦！")
	article_with_type = Article.objects.filter(article_type = type, is_deleted = False)
	#分页器
	paginator = Paginator(article_with_type, 10)
	#获取网址参数
	current_page_para = request.GET.get('page', 1)
	#当前页
	current_page = paginator.get_page(current_page_para)
	#当前页码
	current_page_num = current_page.number
	#展示页码
	display_num = range(max(current_page_num-3, 1), min(current_page_num+4, paginator.page_range[-1]+1))
	content['blogs'] = current_page.object_list
	content['this_page'] = current_page
	content['page_range'] = display_num
	content['articles'] = article_with_type
	content['blog_type']=type
	return render(request, 'blogs_with_type.html', content)
	
def article_with_date(request, year, month):
	page_num=request.GET.get('page',1)
	articles = Article.objects.filter(create_time__year=year, create_time__month=month, is_deleted=False)
	paginator = Paginator(articles,10)
	page_of_blogs = paginator.get_page(page_num)
	current_page = page_of_blogs.number
	display_num = range(max(current_page-3, 1), min(current_page+4, paginator.page_range[-1]+1))
	blog_dates = Article.objects.dates('create_time', 'month', order='DESC')
	context={}
	context['title'] = '%s年%s月' %(year, month)
	context['num'] = articles
	context['articles'] = page_of_blogs.object_list
	context['page_of_blogs'] = page_of_blogs
	context['page_range'] = display_num
	context['blog_dates'] = blog_dates
	return render(request, 'article_with_date.html', context)