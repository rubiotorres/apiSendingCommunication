from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^scheduling/search/(?P<pk>[0-9]+)$', views.SchedulingList.as_view(), name='scheduling-list'),
    url(r'^scheduling/create/$', views.SchedulingCreate.as_view(), name='scheduling-create')
]