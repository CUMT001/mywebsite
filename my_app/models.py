from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class ArticleType(models.Model):
	typename = models.CharField(max_length=20)
	
	def __str__(self):
		return self.typename


class Article(models.Model,ReadNumExpandMethod):
	title = models.CharField(max_length=30)
	article_type = models.ForeignKey(ArticleType, on_delete=models.DO_NOTHING, default=1)
	content = RichTextUploadingField()
	create_time = models.DateTimeField()
	auth = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
	read_details = GenericRelation(ReadDetail)
	is_deleted = models.BooleanField(default=False)
	
	def __str__(self):
		return "<Article:%s>" % self.title
		
	class Meta:
		ordering=['-create_time']
	