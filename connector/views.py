from django.shortcuts import render
from django.http import HttpResponse
from .models import Website, Result
from django.utils import timezone
import subprocess

# Create your views here.
def index(request):
    website_list = Website.objects.all()
    for each in website_list:
        if len(each.result_set.all()) > 0:
            each.result = each.result_set.order_by('-ping_time')[0]
        else:
            pingwebsite(each)
            each.result = each.result_set.order_by('-ping_time')[0]
    context = {
    'website_list': website_list
    }
    return render(request, 'connector/index.html', context)

def ping(request, website):
    pass

def pingwebsite(website):
    url = website.website_url
    sent, returns, avg = pingfunction(url)
    website.result_set.create(ping_time=timezone.now(), ping_success=returns, ping_total=sent, ping_result=avg)

def pingfunction(url):
    result = subprocess.run(['ping', '-c 5', '-W 2', url], stdout=subprocess.PIPE)
    text = result.stdout.decode('ascii')
    texts = text.split('\n')[-4:]
    if '---' in texts[0]:
        stustr = texts[1]
        stastr = texts[2]
    else:
        stustr = texts[2]
        stastr = False
    lstustr = stustr.split(',')
    sent = int(lstustr[0].strip(" ")[0])
    returns = int(lstustr[1].strip(" ")[0])
    if not stastr is False:
        lstastr = stastr.split('/')
        avg = lstastr[-3]
    else:
        avg = -1
    return sent, returns, avg

result = pingfunction('baidu.com')[-4:]
result
