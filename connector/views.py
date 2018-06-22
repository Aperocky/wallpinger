from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Website, Result
from django.utils import timezone
import subprocess

# Create your views here.
def index(request):
    website_list = Website.objects.filter(website_submitter=True)
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
        # if each.result.ping_total == 0:
        #     each.result.failure = True
    context = {
    'website_list': website_list
    }
    return render(request, 'connector/index.html', context)

def ping(request, website_id):
    my_website = Website.objects.get(pk=website_id)
    sent, returns, avg, curr_time = pingwebsite(my_website)
    if returns == 5:
        color = "bg-lime"
    elif returns > 0:
        color = "bg-yellow"
    else:
        color = "bg-red"
    response = {
    'received' : returns,
    'average' : avg,
    'sent_time' : curr_time,
    'color' : color
    }
    return JsonResponse(response)

def history(request, website_id):
    my_website = Website.objects.get(pk=website_id)
    records = my_website.result_set.all().order_by('-ping_time')
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

def add_website(request):
    website_name = request.POST['website_name']
    website_url = request.POST['website_url']
    my_website = Website(website_name=website_name, website_url=website_url, website_submitter=False)
    my_website.save()
    my_id = my_website.pk
    sent, returns, avg, curr_time = pingwebsite(my_website)
    if returns == 5:
        color = "bg-lime"
    elif returns > 0:
        color = "bg-yellow"
    else:
        color = "bg-red"
    response = {
    'website_name': my_website.website_name,
    'website_url': my_website.website_url,
    'received' : returns,
    'sent': sent,
    'average' : avg,
    'sent_time' : curr_time,
    'color' : color,
    'my_id' : my_id
    }
    if sent == 0:
        my_website.delete()
    return JsonResponse(response)

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
    print(texts)
    if '---' in texts[0]:
        stustr = texts[1]
        stastr = texts[2]
    else:
        if len(texts) < 3:
            stustr = "0 of 0, This probably is not a valid URL"
        else:
            stustr = texts[2]
        stastr = False
    lstustr = stustr.split(',')
    sent = int(lstustr[0].strip(" ")[0])
    returns = int(lstustr[1].strip(" ")[0])
    if not stastr is False:
        lstastr = stastr.split('/')
        if len(lstastr) > 3:
            avg = lstastr[-3]
        else:
            avg = -1
    else:
        avg = -1
    return sent, returns, avg
