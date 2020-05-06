from django.contrib.sitemaps import Sitemap

from .models import Story


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Story.published.all()

    def lastmod(self, obj):
        return obj.created
