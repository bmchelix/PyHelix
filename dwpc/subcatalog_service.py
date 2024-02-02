import json
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import SUB_CATALOGS_PATH

_LOGGER = logger.get_logger(__name__)


class SubCatalogService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_sub_catalogs(self):
        url = f"{self.url}{SUB_CATALOGS_PATH}?page=1&perPage=20&search=&sortBy=modifiedDate&sortDirection=desc"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get subCatalogs"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
