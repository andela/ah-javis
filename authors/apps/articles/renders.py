import json
from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if data is not None:

            if isinstance(data, dict):
                return json.dumps({
                    'article': data
                })
            return json.dumps({
                'articles': data,
                'articlesCount': len(data)
            })
        return json.dumps({
            "article": 'No article found.'
        })

class CommentJSONRenderer(JSONRenderer):
    """ renders comments"""
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'comments': data
                })
            return json.dumps({
                'comment': data
            })
        return json.dumps({
            "comment": 'No article found.'
        }
        

class RateJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the ratings in a structured manner for the end user.
        """
        return json.dumps({
            'rate': data,
        })
