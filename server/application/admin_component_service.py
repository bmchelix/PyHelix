import json
from utils import logger

from requests import status_codes

from commons import connector
from server.constants import PATH_OF_RX_APP_DATAPAGE, REQUEST_OVERLAY_GROUP, DEFAULT_BUNDLE_SCOPE
from server.constants import ADMIN_COMPONENT_DATA_PAGE_QUERY, ADMIN_COMPONENT_PATH

_LOGGER = logger.get_logger(__name__)


class AdminComponentServiceImpl:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_admin_component_setings(self, component_name):
        url = f"{self.url}{ADMIN_COMPONENT_PATH}/{component_name}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get admin component information : {component_name},  "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_admin_components_details(self, bundle_scope, **kwargs):
        page_size = kwargs.get('pageSize', 1)
        start_index = kwargs.get('startIndex', 0)
        request_overlay_group = kwargs.get('request_overlay_group', "1")
        url = f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={ADMIN_COMPONENT_DATA_PAGE_QUERY}&startIndex={start_index}&pageSize={page_size}"
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_scope
        connector.headers[REQUEST_OVERLAY_GROUP] = request_overlay_group
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to make admin component dataPage query for bundleScope: {bundle_scope},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response
