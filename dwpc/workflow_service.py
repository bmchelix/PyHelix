import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import SUB_CATALOG_WORKFLOWS

_LOGGER = logger.get_logger(__name__)


class WorkflowService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_workflows(self):
        url = f"{self.url}{SUB_CATALOG_WORKFLOWS}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get workflows"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
