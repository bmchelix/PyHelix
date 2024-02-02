from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import CONTENT_PATH

_LOGGER = logger.get_logger(__name__)


class ContentService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_content(self, content_id):
        url = f"{self.url}{CONTENT_PATH}/{content_id}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get content by id : {content_id}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = response.content
        return result
