import json
from utils import logger

from requests import status_codes
from commons import connector

_LOGGER = logger.get_logger(__name__)


class ActivityLogService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_request_activities(self, request_id):
        url = f"{self.url}/api/myit-sb/services/requests/{request_id}/activities"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get activities for request Id : {request_id}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
