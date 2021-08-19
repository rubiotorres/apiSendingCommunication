from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^scheduling/$', views.SchedulingList.as_view(), name='scheduling-list'),
]