# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from notifications.signals import notify
# from celery import shared_task
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from authors.apps.articles.models import Article
# from authors.apps.core.email import SendMail


# @receiver(post_save, sender=Article)
# def send_notifications_if_(sender, instance, created, *args, **kwargs):

#     if instance and created:
#         followers = [p.user for p in instance.author.followed_by.all()]
#         notify.send(instance, recipient=followers,
#                     verb='A new article have been published')
#         SendMail(
#             template_name="articles/new_article.html",
#             context={
#                 "article": instance
#             },
#             subject=instance.author.user.username + " has published a new article",
#             to=[u.email for u in followers],
#         ).send()
