from django.urls import path, include
from . import views

app_name = 'story'


urlpatterns = [

	url(r'^new-story/$',
		views.create,
		name='create'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/stories/$',
		views.list,
		name='list'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/stories/drafts/$',
		views.drafts,
		name='drafts'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/stories/bookmarks/$',
		views.bookmarks,
		name='bookmarks'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/stories/favorites/$',
		views.favorites,
		name='favorites'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/(?P<slug>[-\w]+)-(?P<id>\d+)/$',
		views.detail,
		name='detail'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/(?P<slug>[-\w]+)-(?P<id>\d+)/edit/$',
		views.edit,
		name='edit'),

	url(r'^accounts/(?P<username>[\w.@+-]+)/(?P<slug>[-\w]+)-(?P<id>\d+)/delete/$',
		views.delete,
		name='delete'),

	url(r'^(?P<id>\d+)/feature/$',
		views.feature,
		name='feature'),

	url(r'^(?P<id>\d+)/save/$',
		views.add_bookmark,
		name='add_bookmark'),

	url(r'^(?P<id>\d+)/unsave/$',
		views.delete_bookmark,
		name='delete_bookmark'),

	url(r'^(?P<id>\d+)/favorite/$',
		views.favorite,
		name='favorite'),

	url(r'^(?P<id>\d+)/unfavorite/$',
		views.unfavorite,
		name='unfavorite'),

	# url(r'^accounts/(?P<username>[\w.@+-]+)/(?P<slug>[-\w]+)-(?P<id>\d+)/favorite/$',
	# 	views.favorite,
	# 	name='favorite'),
	# url(r'^like/$', 
	# 	views.image_like, 
	# 	name='like'),
]


urlpatterns = [
    path('favorite/', views.story_favorite, name='favorite'),
    path('save/', views.story_bookmark, name='save'),
    path('new-story/', views.create, name='create'),

    path('accounts/<username>/stories/', views.list, name='list'),
    path('accounts/<username>/stories/drafts/', views.drafts, name='drafts'),
    path('accounts/<username>/stories/bookmarks/',
         views.bookmarks, name='bookmarks'),
    path('accounts/<username>/stories/favorites/',
         views.favorites, name='favorites'),

    # path('<int:id>/feature/',
    # 	views.feature,
    # 	name='feature'),
    path('accounts/<username>/', include([
        path('stories/', views.list, name='list'),
        path('<slug:slug>-<int:id>/', views.detail, name='detail'),
        path('<slug:slug>-<int:id>/edit/', views.edit, name='edit'),
        # path('<slug:slug>-<int:id>/delete/', views.delete, name='delete'),
    ]))
]

# www.footystory.com/pythonian/stories/
# www.footystory.com/pythonian/stories/drafts/
# www.footystory.com/pythonian/stories/bookmarks/
# www.footystory.com/pythonian/stories/my-footy-story-20
# www.footystory.com/pythonian/stories/my-footy-story-23/edit/
# www.footystory.com/pythonian/stories/my-footy-story-23/delete/
