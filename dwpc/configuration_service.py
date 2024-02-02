import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import TICKET_TEMPLATES_PATH, SERVICE_COMPANIES_PATH

_LOGGER = logger.get_logger(__name__)


class ConfigurationService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_ticket_templates(self, **kwargs):
        external_sub_catalog_id = kwargs.get('externalSubCatalogId', None)
        if external_sub_catalog_id:
            connector.headers["X-DWP-SubCatalog"] = external_sub_catalog_id
        url = f"{self.url}{TICKET_TEMPLATES_PATH}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get ticket templates, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_companies(self):
        url = f"{self.url}{SERVICE_COMPANIES_PATH}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get companies, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
