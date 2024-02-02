import json
from utils import logger

from requests import status_codes

from commons import connector
from server.application.copy_definition_command import CopyDefinitionServiceImpl
from server.constants import PROCESS_DEFINITION_PATH, DEFAULT_BUNDLE_SCOPE, REQUEST_OVERLAY_GROUP
from server.constants import PATH_OF_RX_APP_DATAPAGE
from server.constants import PATH_OF_RX_APP_COMMAND
from server.constants import PROCESS_INSTANCE_PATH
from server.constants import PROCESS_INSTANCE_DATA_PAGE_QUERY
from server.constants import PROCESS_INSTANCE_COUNTS_BY_STATUS_DATA_PAGE_QUERY

_LOGGER = logger.get_logger(__name__)


class ProcessServiceImpl:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()
        self.copy_definition_service = CopyDefinitionServiceImpl(connection)

    def get_process_definition(self, process_definition_name, **kwargs):
        request_overlay_group = kwargs.get('request_overlay_group', "1")
        connector.headers[REQUEST_OVERLAY_GROUP] = request_overlay_group
        url = f"{self.url}{PROCESS_DEFINITION_PATH}/{process_definition_name}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get process definition : {process_definition_name},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        return json.loads(response.content)

    def execute_process_instance(self, process_name, inputs):
        url = f"{self.url}{PATH_OF_RX_APP_COMMAND}"
        body_request = {'processDefinitionName': process_name,
                        'resourceType': "com.bmc.arsys.rx.application.process.command.StartProcessInstanceCommand",
                        'processInputValues': {}}
        for key, value in inputs.items():
            body_request['processInputValues'][key] = value
        response = self.session.post(url=url, data=json.dumps(body_request), headers=connector.headers)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (
                f"Failed to execute process definition : {process_name},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        return response.headers['Location']

    def get_process_instance(self, process_definition_name, process_id):
        url = f"{self.url}{PROCESS_INSTANCE_PATH}/{process_definition_name}/{process_id}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get process instance : {process_definition_name},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        return json.loads(response.content)

    def get_process_instances(self, bundle_id, **kwargs):

        proces_definition = kwargs.get('procesDefinition', None)
        page_size = kwargs.get('pageSize', 2000)
        start_index = kwargs.get('startIndex', 0)
        status = kwargs.get('status', "COMPLETED")
        started_after = kwargs.get('startedAfter', None)

        url = f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={PROCESS_INSTANCE_DATA_PAGE_QUERY}&startIndex={start_index}&pageSize={page_size}&propertySelection=contextKey%2CinstanceId%2CprocessDefinitionName%2Cowner%2CstartTime%2CendTime%2Cstatus&sortBy=-startTime&status={status}"
        if started_after is not None:
            url = url + "&startedAfter=" + str(started_after)
        if proces_definition:
            url = url + "&processDefinitionName=" + 'com.bmc.dsm.case-lib:Case - On Load Perform Actions'
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_id
        connector.headers[REQUEST_OVERLAY_GROUP] = "1"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get process instances for bundleId: {bundle_id},  "
                f"status : {status}, startedAfter : {started_after}, response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response

    def get_process_instances_count(self, bundle_scope, query_expression=None):
        url = (
            f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={PROCESS_INSTANCE_COUNTS_BY_STATUS_DATA_PAGE_QUERY}&startIndex=0&pageSize=-1&startedAfter=2024-01-29T15:20:53.487Z")
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_scope
        connector.headers[REQUEST_OVERLAY_GROUP] = "1"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get process instances count with queryExpression: {query_expression},  "
                f"queryExpression : {query_expression}, response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response

    def copy_process_definition(self, src_name, dest_name, **kwargs):
        return self.copy_definition_service.copy_workflow_definition("PROCESS_DEFINITION", src_name, dest_name, **kwargs)
