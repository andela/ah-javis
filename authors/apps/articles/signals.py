from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from authors.apps.articles.models import Article
from authors.apps.core.email import SendMail

@receiver(post_save, sender=Article)
def send_notifications_to_followers(sender, instance, created, *args, **kwargs):

    if instance and created:
        followers = [p.user for p in instance.author.followed_by.all()]
        notify.send(instance, recipient=followers,  verb='A new article have been published')