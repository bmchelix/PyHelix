import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import CONNECTION_PATH

_LOGGER = logger.get_logger(__name__)


class ConnectorService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_connectors(self):
        url = f"{self.url}{CONNECTION_PATH}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get connectors, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def ping_connector(self, connector_id):
        url = f"{self.url}{CONNECTION_PATH}/{connector_id}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to ping connector, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
