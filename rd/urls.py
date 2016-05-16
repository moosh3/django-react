from django.conf.urls import url, include
from rd.views import index


urlpatterns = [
    url(r'^', index, name='index'),
]
