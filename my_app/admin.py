from django.contrib import admin
from .models import Article, ArticleType

# Register your models here.
# 此类用于自定义显示后台管理界面的显示,list_display表示显示的内容,ordering指定排序方式,也可以在外部编写函数用于对对象进行操作,在类的内部使用actions明确操作,参见https://docs.djangoproject.com/en/2.1/ref/contrib/admin/actions/
# @admin.register(Article)此句等价于admin.site.register(Article, ArticleAdmin)是python中的装饰器的写法
class ArticleAdmin(admin.ModelAdmin):
	list_display = ("title", "article_type", "get_read_num", "auth")
	
class ArticleTypeAdmin(admin.ModelAdmin):
	list_display = ("id","typename")
	
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleType, ArticleTypeAdmin)