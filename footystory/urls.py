from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^', include('story.urls', namespace='story')),
    url(r'^topics/', include('topics.urls', namespace='topics')),
    url(r'^people/$', views.people, name='people'),
    url(r'^stories/$', views.stories, name='stories'),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #      name='sitemap'),
    url(r'^$', views.home, name='home'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('admin/doc/', include('django.contrib.admindocs.urls')),
#     path('admin/', admin.site.urls),
#     path('account/', include('account.urls')),
#     path('', home, name='home'),
# ]

# from story.sitemaps import StorySitemap

# sitemaps = {
#     'story': StorySitemap,
# }
