import json
from utils import logger

from requests import status_codes

from commons import connector
from server.constants import PATH_OF_RX_APP_DATAPAGE, DEFAULT_BUNDLE_SCOPE, REQUEST_OVERLAY_GROUP
from server.constants import ASSOCIATION_DEFINITION_PATH
from server.constants import ASSOCIATION_DEFINITION_DATA_PAGE_QUERY

_LOGGER = logger.get_logger(__name__)


class AssociationServiceImpl:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def get_association_definition(self, association_definition_name):
        url = f"{self.url}{ASSOCIATION_DEFINITION_PATH}/{association_definition_name}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get association definition : {association_definition_name},  "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_association_definitions_details(self, bundle_scope, **kwargs):
        page_size = kwargs.get('pageSize', -1)
        start_index = kwargs.get('startIndex', 0)
        request_overlay_group = kwargs.get('request_overlay_group', "1")
        bundle_id = kwargs.get('bundleId')
        property_selections = "name,nodeAId,cardinality,nodeBId,shouldCascadeDelete,lastUpdateTime,lastChangedBy,customizationPerspective,isEnabled,scope,overlayGroupId,overlayDescriptor"
        url = f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={ASSOCIATION_DEFINITION_DATA_PAGE_QUERY}&startIndex={start_index}&pageSize={page_size}&propertySelection={property_selections}"
        if bundle_id:
            url = url + "&bundleId={bundleId}"
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_scope
        connector.headers[REQUEST_OVERLAY_GROUP] = request_overlay_group
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to make association definition dataPage query for bundleScope: {bundle_scope},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response
