from django.conf.urls import url
from markupApp import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_block/$', views.add_block, name='add_block'),
]
