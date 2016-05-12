from django.conf.urls import url, include
from django.views.generic import TemplateView
from rd.views import comment_box, comment


urlpatterns = [
    url(r'^', comment_box, name='index'),
    url(r'^comment/$', comment, name='comment'),
]
