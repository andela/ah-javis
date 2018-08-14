""" Core mail sender"""
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from celery import shared_task, Task
from authors.celery import app


class SendMail(Task):
    """ Send email to user """
    ignore_result = True
    name = "send_email"

    def __init__(self, template_name=None, context=None, to=None, subject="Author's Haven", user_request=None):
        super(SendMail).__init__()
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
    def run(self, source, *args, **kwargs):
        self.source = source
        mail = EmailMessage(
            subject=self.subject, body=self.message, to=self.to
        )
        mail.content_subtype = "html"
        mail.send()

  


app.tasks.register(SendMail())
