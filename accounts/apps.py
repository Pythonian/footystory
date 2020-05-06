from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
    	import accounts.signals
		from .checks import settings_check
