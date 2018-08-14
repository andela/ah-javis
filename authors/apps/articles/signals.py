from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from authors.apps.articles.models import Article, Comment
from authors.apps.core.email import SendMail


@receiver(post_save, sender=Article)
def send_notifications_to_followers(sender, instance, created, *args, **kwargs):

    if instance and created:
        followers = [p.user for p in instance.author.followed_by.all()]
        notify.send(instance, recipient=followers,
                    verb='A new article have been published')
        SendMail(
            template_name="articles/new_article.html",
            context={
                "article": instance
            },
            subject=instance.author.user.username + " has published a new article",
            to=[u.email for u in followers],
        ).send()


@receiver(post_save, sender=Comment)
def send_notifications_when_commented(sender, instance, created, *args, **kwargs):

    if instance and created:
        # followers = [p.user for p in instance.author.followed_by.all()]
        users = [u.user for u in instance.article.users_favorites.all()]
        notify.send(instance, recipient=users,
                    verb='A new article have been published')
        SendMail(
            template_name="articles/alert_comment.html",
            context={
                "article": instance.article,
                "comment": instance
            },
            subject=instance.author.user.username + " has commented on article",
            to=[u.email for u in users],
        ).send()
