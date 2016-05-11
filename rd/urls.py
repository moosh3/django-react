from django.conf.urls import url, include
from django.views.generic import TemplateView
from rd.views import rendered_index


urlpatterns = [
    url(r'^', rendered_index, name='index')
]
