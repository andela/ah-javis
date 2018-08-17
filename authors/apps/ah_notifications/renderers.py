import json

from authors.apps.core.renderers import AuthorsJSONRenderer


class NotificationJSONRenderer(AuthorsJSONRenderer):
    charset = 'utf-8'
    object_label = "notification"
    object_label_plural = "notifications"
