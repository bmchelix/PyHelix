import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import SERVICE_SEARCH

_LOGGER = logger.get_logger(__name__)


class ServiceCatalogService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_services(self, **kwargs):
        sub_catalog_id = kwargs.get('subCatalogId', None)
        if sub_catalog_id:
            payload = {"serviceName": "", "subCatalogIds": [sub_catalog_id]}
        else:
            payload = {"serviceName": "", "subCatalogIds": []}
        url = f"{self.url}{SERVICE_SEARCH}?page=1&perPage=2000&sortBy=modifiedDate&sortDirection=desc"
        response = self.session.post(url=url, data=json.dumps(payload), headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get services"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
