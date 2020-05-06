from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$',
		views.list,
		name='list'),

	url(r'^my-topics/$',
		views.user_topics,
		name='user_topics'),

	url(r'^(?P<slug>[-\w]+)/$',
		views.detail,
		name='detail'),

	url(r'^(?P<id>\d+)/like/$',
		views.like,
		name='like'),

	url(r'^(?P<id>\d+)/unlike/$',
		views.unlike,
		name='unlike'),

]

# from django.urls import path
# from . import views

# app_name = 'topic'

# urlpatterns = [
#     path('like/', views.topic_like, name='like'),
#     path('<slug>/', views.detail, name='detail'),
#     path('', views.list, name='list'),
#     # path('my-topics/', views.user_topics, name='user_topics'),
#     # path('<int:id>/like/', views.like, name='like'),
#     # path('<int:id>/unlike/', views.unlike, name='unlike'),
# ]
