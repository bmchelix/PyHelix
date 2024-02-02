import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import SERVICE_REQUEST_PATH

_LOGGER = logger.get_logger(__name__)


class SubCatalogService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_questionnaire_by_request_id(self, request_id):
        url = f"{self.url}{SERVICE_REQUEST_PATH}/{request_id}/questionnaire"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get questionnaire for request Id : {request_id}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_questionnaire(self, questionnaire_id):
        url = f"{self.url}/api/myit-sb/questionnaires/ml/{questionnaire_id}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get questionnaire : {questionnaire_id}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
