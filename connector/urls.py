from django.urls import path

from . import views

app_name = 'connector'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:website_id>/ping', views.ping, name='ping'),
    path('<int:website_id>/history', views.history, name='history')
]
