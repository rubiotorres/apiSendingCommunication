from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    url(r'^scheduling/status/id/(?P<pk>[0-9]+)$', views.SchedulingSearchId.as_view(), name='scheduling-get'),
    url(r'^scheduling/search/$', views.SchedulingSearchList.as_view(), name='scheduling-list'),
    url(r'^scheduling/create/$', views.SchedulingCreate.as_view(), name='scheduling-create'),
    url(r'^scheduling/delete/id/(?P<pk>[0-9]+)$', views.SchedulingDelete.as_view(), name='scheduling-delete'),
    # Get Token auth
    url(r'^scheduling/api-token-auth/', obtain_auth_token, name='api_token_auth')
]
