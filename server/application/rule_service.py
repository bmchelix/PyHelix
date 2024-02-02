import json
from utils import logger

from requests import status_codes

from commons import connector
from server.application.copy_definition_command import CopyDefinitionServiceImpl
from server.constants import PATH_OF_RX_APP_DATAPAGE, REQUEST_OVERLAY_GROUP, DEFAULT_BUNDLE_SCOPE
from server.constants import RULE_DEFINITION_PATH
from server.constants import RULE_DEFINITION_DATA_PAGE_QUERY

_LOGGER = logger.get_logger(__name__)


class RuleServiceImpl:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()
        self.copy_definition_service = CopyDefinitionServiceImpl(connection)

    def get_rule_definition(self, rule_definition_name):
        url = f"{self.url}{RULE_DEFINITION_PATH}/{rule_definition_name}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get rule definition : {rule_definition_name}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_rule_definitions_details(self, bundle_scope, **kwargs):
        page_size = kwargs.get('pageSize', -1)
        start_index = kwargs.get('startIndex', 0)
        request_overlay_group = kwargs.get('request_overlay_group', "1")
        bundle_id = kwargs.get('bundleId')
        property_selections = "name,recordDefinitionNames,triggerEvent,lastUpdateTime,lastChangedBy,isEnabled,scope,customizationPerspective,overlayGroupId"
        url = f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={RULE_DEFINITION_DATA_PAGE_QUERY}&startIndex={start_index}&pageSize={page_size}&propertySelection={property_selections}"
        if bundle_id:
            url = url + "&bundleId={bundleId}"
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_scope
        connector.headers[REQUEST_OVERLAY_GROUP] = request_overlay_group
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to make rule definition dataPage query for bundleScope: {bundle_scope}, "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response

    def copy_rule_definition(self, src_name, dest_name, **kwargs):
        return self.copy_definition_service.copy_workflow_definition("RULE_DEFINITION", src_name, dest_name, **kwargs)
