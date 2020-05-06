from __future__ import unicode_literals

from django.apps import AppConfig


class TopicsConfig(AppConfig):
    name = 'topics'

    verbose_name = 'Topics'

    def ready(self):
    	# import signal handlers
    	import topics.signals