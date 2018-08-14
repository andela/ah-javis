""" Core mail sender"""
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from celery import shared_task, Task
from celery.utils.log import get_task_logger
from celery import shared_task
from authors.celery import app

logger = get_task_logger('send_mail')


@shared_task
def send_mail(content):
    mail = EmailMessage(
        subject=content['subject'], body=content['message'], to=content['to']
    )
    mail.content_subtype = "html"
    mail.send()


class SendMail():
    """ Send email to user """

    def __init__(self, template_name=None, context=None, to=None, subject="Author's Haven", user_request=None):
        self.template_name = template_name
        self.context = context
        self.to = to
        self.subject = subject
        self.user_request = user_request
        self.mail = None
        if self.template_name is not None:
            self.message = render_to_string(
                self.template_name, context=self.context, request=self.user_request)
        else:
            self.message = None

    def send(self):
        content = {
            "subject": self.subject,
            "to": self.to,
            "message": self.message
        }
        send_mail.delay(content)
