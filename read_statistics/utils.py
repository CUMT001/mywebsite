from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum, ReadDetail
import datetime
from django.db.models import Sum

def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" % (ct.model, obj.id)
	if not request.COOKIES.get(key):
		readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.id)
		readnum.read_num += 1
		readnum.save()
		
		if ReadDetail.objects.filter(content_type=ct, object_id=obj.id, date=timezone.now().date()).count():
			read_detail = ReadDetail.objects.filter(content_type=ct, object_id=obj.id, date=timezone.now().date())
		else:
			read_detail = ReadDetail(content_type=ct, object_id=obj.id, date=timezone.now().date())
		read_detail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=timezone.now().date())
		read_detail.read_num += 1
		read_detail.save()
	return key
	
def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	dates = []
	read_nums = []
	for i in range(6,-1,-1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)
	return dates,read_nums
	
def get_today_hot_data(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
	return read_details[:5]
	
def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today-datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
	return read_details
	
def get_7_days_hot_data(content_type):
	today = timezone.now().date()
	date = today-datetime.timedelta(days=7)
	read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gte=date).values('content_type', 'object_id').annotate(read_num_sum=Sum('read_num')).order_by('-read_num_sum')
	return read_details