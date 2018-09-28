from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^page/(?P<pk>\d+)$', views.PageDetailView.as_view(), name='page_detail'),
    url(r'^my_pages/$', views.my_pages, name='my_pages'),
    # url(r'^search/$', views.SearchListView.as_view(), name='search_list_view'),
    # url(r'^pages/$', views.PageListView.as_view(), name='page_list'),
    url(r'^student/create/$', views.StudentCreate.as_view(), name='student_create'),
]

