from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Website, Result
from django.utils import timezone
import subprocess

# Create your views here.
def index(request):
    website_list = Website.objects.all()
    for each in website_list:
        each.condensed_name = each.website_name.replace(" ", "")
        if len(each.result_set.all()) > 0:
            each.result = each.result_set.order_by('-ping_time')[0]
        else:
            pingwebsite(each)
            each.result = each.result_set.order_by('-ping_time')[0]
        if each.result.ping_result == -1:
            each.result.ping_result = "N/A"
        else:
            each.result.ping_result = str(each.result.ping_result)
            each.result.ping_result += " ms"
        if each.result.ping_success == 5:
            each.result.color = "bg-lime"
        elif each.result.ping_success > 0:
            each.result.color = "bg-yellow"
        else:
            each.result.color = "bg-red"
    context = {
    'website_list': website_list
    }
    return render(request, 'connector/index.html', context)

def ping(request, website_id):
    my_website = Website.objects.get(pk=website_id)
    sent, returns, avg, curr_time = pingwebsite(my_website)
    resdata = {
    'received' : returns,
    'average' : avg,
    'sent_time' : curr_time
    }
    return JsonResponse(resdata)

def history(request, website_id):
    my_website = Website.objects.get(pk=website_id)
    records = my_website.result_set.all()
    for each in records:
        each.ping_result = str(each.ping_result)
        each.ping_result += " ms"
        if each.ping_success == 5:
            each.color = "bg-lime"
        elif each.ping_success > 0:
            each.color = "bg-yellow"
        else:
            each.color = "bg-red"
    context = {
    'website' : my_website,
    'records' : records
    }
    return render(request, 'connector/history.html', context)

def pingwebsite(website):
    url = website.website_url
    sent, returns, avg = pingfunction(url)
    curr_time = timezone.now()
    website.result_set.create(ping_time=curr_time, ping_success=returns, ping_total=sent, ping_result=avg)
    return sent, returns, avg, curr_time

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
