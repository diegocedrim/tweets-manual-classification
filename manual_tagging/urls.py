from django.conf.urls import url

from . import views

app_name = 'manual_tagging'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^next_tweets/(?P<size>[0-9]+)/$', views.next_tweets, name='next_tweets'),
    url(r'^load_tweet/(?P<tag_id>[0-9]+)/$', views.load_single_tag, name='load_single_tag'),
    url(r'^save_single/$', views.save_single_tag, name='save_single'),
    url(r'^save_tags/$', views.save_tags, name='save_tags'),
    url(r'^latest_classified/$', views.latest_classified, name='latest_classified'),
]