from django.apps import AppConfig


class StoryConfig(AppConfig):
    name = 'story'

    def ready(self):
    	# import signal handlers
    	import story.signals
