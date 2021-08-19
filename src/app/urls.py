from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^scheduling/search/id/(?P<pk>[0-9]+)$', views.SchedulingSearchId.as_view(), name='scheduling-get'),
    url(r'^scheduling/search/$', views.SchedulingSearchList.as_view(), name='scheduling-list'),
    url(r'^scheduling/create/$', views.SchedulingCreate.as_view(), name='scheduling-create'),
    url(r'^scheduling/delete/(?P<pk>[0-9]+)$', views.SchedulingDelete.as_view(), name='scheduling-delete'),
]