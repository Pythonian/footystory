from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Topic


@receiver(m2m_changed, sender=Topic.users_likes.through)
def users_likes_changed(sender, instance, **kwargs):
	# Call the function if the signal has been launched by the sender
	instance.likes = instance.users_likes.count()
	instance.save()

