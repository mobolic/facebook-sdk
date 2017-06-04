from django.conf.urls import include, url
from django.contrib import admin

from blog import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post, name='post-detail'),
]
