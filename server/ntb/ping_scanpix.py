
import requests

from flask import json
from superdesk.signals import item_published


SCANPIX_PING_URL = 'https://api.sdl.no/v1/pushData'


def handle_item_published(sender, item, **kwargs):
    if item.get('associations'):
        for key, assoc in item['associations'].items():
            if assoc is not None and assoc.get('fetch_endpoint') == 'scanpix':
                requests.post(
                    SCANPIX_PING_URL,
                    json.dumps({
                        'type': 'articleUsage',
                        'data': {
                            'media_id': assoc.get('guid', assoc.get('_id')),
                            'article_id': item.get('guid', item.get('_id')),
                        },
                    }),
                    headers={'content-type': 'application/json'},
                )


def init_app(app):
    if app.config.get('SCANPIX_PING'):
        item_published.connect(handle_item_published)
