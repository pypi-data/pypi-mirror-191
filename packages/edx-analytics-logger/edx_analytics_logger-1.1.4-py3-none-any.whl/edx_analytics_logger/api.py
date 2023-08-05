"""Api Analytics event tracker backend.
"""
import json
import logging
import requests

from celery import shared_task
from common.djangoapps.track.backends import BaseBackend
from common.djangoapps.track.utils import DateTimeJSONEncoder


logger = logging.getLogger(__name__)


@shared_task
def send_event_tracking_log(event_str, endpoint, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    r = requests.post(endpoint, data=event_str, headers=headers)
    try:
        r.raise_for_status()
    except Exception as e:
        # Log the error to be able to debug, then raise again exception
        logger.exception("Got %s status code. Text: %s", r.status_code, r.text)
        logger.exception(e)
        raise e


class ApiBackend(BaseBackend):

    def __init__(self, endpoint, token, **kwargs):
        """Event tracker backend to send payloads to a remote endpoint.
        :Parameters:
          - `endpoint`: URI endpoint which should receive the event.
          - `token`: Value to authenticate against endpoint defined.
        """
        self.endpoint = endpoint
        self.token = token
        super().__init__(**kwargs)

    def send(self, event):
        event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        send_event_tracking_log.delay(event_str, self.endpoint, self.token)
