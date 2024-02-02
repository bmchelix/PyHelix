import json
from utils import logger
import math
from typing import Set
from urllib.parse import urlencode

from requests import status_codes

from commons import connector
from commons.connector import headers
from server.application.copy_definition_command import CopyDefinitionServiceImpl
from server.application.record_instance import Attachment
from server.constants import PATH_OF_RX_APP_DATAPAGE, DEFAULT_BUNDLE_SCOPE, REQUEST_OVERLAY_GROUP
from server.constants import RECORD_DEFINITION_PATH
from server.constants import RX_ATTACHMENT_PATH
from server.constants import RECORD_INSTANCE_PATH
from server.constants import RECORD_INSTANCE_DATA_PAGE_QUERY

_LOGGER = logger.get_logger(__name__)


class RecordServiceImpl:
    __DEFAULT_QUERY_PAGE_SIZE = 200

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()
        self.copy_definition_service = CopyDefinitionServiceImpl(connection)

    @classmethod
    def get_default_query_page_size(cls):
        return cls.__DEFAULT_QUERY_PAGE_SIZE

    def get_record_instances_bulk(self, record_definition_name, **kwargs):
        query_expression = kwargs.get('queryExpression', None)
        property_selection_fields = kwargs.get('propertySelectionFields', None)
        sort_by = kwargs.get('"sortBy', None)
        query_page_size = kwargs.get('queryPageSize', self.get_default_query_page_size())
        query_params = {}
        total_number_of_records = self.get_record_instances_count(record_definition_name, query_expression)
        query_params['shouldIncludeTotalSize'] = "true"
        query_params['recorddefinition'] = record_definition_name
        query_params['dataPageType'] = "%s" % RECORD_INSTANCE_DATA_PAGE_QUERY
        query_params['pageSize'] = -1
        query_params['startIndex'] = 0
        if sort_by:
            query_params['sortBy'] = sort_by
        if property_selection_fields:
            query_params['propertySelection'] = property_selection_fields
        if query_expression:
            query_params['queryExpression'] = query_expression
        total_number_of_batches = math.floor(
            total_number_of_records / query_page_size if total_number_of_records % query_page_size == 0 else (total_number_of_records / query_page_size) + 1)
        batch_start_index = 0
        batch_end_index = total_number_of_records + batch_start_index
        result = list()
        for i in range(total_number_of_batches):
            if batch_start_index <= batch_end_index:
                calculated_page_size = query_page_size if (batch_end_index - batch_start_index) >= query_page_size else batch_end_index - batch_start_index
                query_params['pageSize'] = calculated_page_size
                query_params['startIndex'] = batch_start_index
                url = self.url + PATH_OF_RX_APP_DATAPAGE + "?" + urlencode(query_params)
                data_page_response = self.session.get(url=url, headers=headers)
                if data_page_response.status_code != status_codes.codes.OK:
                    error_message = (
                        f"Failed to get record instances for recordDefinitionName : {record_definition_name},  "
                        f"queryExpression : {query_expression}, response code : {data_page_response.status_code} , body : {data_page_response.content}")
                    _LOGGER.error(error_message)
                    raise Exception(error_message)
                json_data_page_response = json.loads(data_page_response.content)
                if json_data_page_response['data'] is None:
                    break
                batch_start_index += query_page_size
                result.extend(json_data_page_response['data'])
        return result

    def get_record_instances(self, record_definition_name, **kwargs):
        sort_by = kwargs.get('sortBy', None)
        property_selection_fields = kwargs.get('propertySelectionFields', None)
        query_expression = kwargs.get('queryExpression', None)
        page_size = kwargs.get('pageSize', -1)
        start_index = kwargs.get('startIndex', 0)
        query_params = {}
        query_params['shouldIncludeTotalSize'] = "true"
        query_params['recorddefinition'] = record_definition_name
        query_params['dataPageType'] = f"{RECORD_INSTANCE_DATA_PAGE_QUERY}"
        if sort_by:
            query_params['sortBy'] = sort_by
        if property_selection_fields:
            query_params['propertySelection'] = property_selection_fields
        if query_expression:
            query_params['queryExpression'] = query_expression
        query_params['pageSize'] = page_size
        query_params['startIndex'] = start_index
        url = self.url + PATH_OF_RX_APP_DATAPAGE + "?" + urlencode(query_params)
        data_page_response = self.session.get(url=url, headers=headers)
        if data_page_response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get record instances for recordDefinitionName : {record_definition_name},  "
                f"queryExpression : {query_expression}, response code : {data_page_response.status_code} , body : {data_page_response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(data_page_response.content)
        return result

    def get_record_instances_count(self, record_definition_name, query_expression=None):
        url = (f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={RECORD_INSTANCE_DATA_PAGE_QUERY}&pageSize=0&"
               f"recorddefinition={record_definition_name}&shouldIncludeTotalSize=true")
        if query_expression is not None:
            url = url + "&queryExpression=" + query_expression
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to get record instances count for recordDefinitionName : {record_definition_name},  "
                f"queryExpression : {query_expression}, response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response['totalSize']

    def get_record_instance(self, record_definition_name, record_instance_id):
        url = f"{self.url}{RECORD_INSTANCE_PATH}/{record_definition_name}/{record_instance_id}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get record instance for recordDefinitionName : {record_definition_name},  "
                             f"recordInstanceId : {record_instance_id}, response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_file(self, record_definition_name, record_instance_id, field_id):
        url = f"{self.url}{RX_ATTACHMENT_PATH}/{record_definition_name}/{record_instance_id}/{field_id}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get file for recordDefinitionName : {record_definition_name},  "
                             f"id : {record_instance_id}, fieldId : {field_id}, response code : {response.status_code} , "
                             f"body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        return response.content

    def create_record_instance(self, record_instance):
        url = f"{self.url}{RECORD_INSTANCE_PATH}"
        response = self.session.post(url=url, data=json.dumps(record_instance.to_json()), headers=connector.headers)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (f"Failed to create record instance : {record_instance},  "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        location = response.headers['Location']
        record_id = location.split("/")[-1]
        return record_id

    def create_record_instance_form_data(self, record_instance, attachments: Set[Attachment]):
        multipart_form_data = {'recordInstance': (None, json.dumps(record_instance.to_json()), None)}
        for attachment in attachments:
            multipart_form_data[attachment.fieldId] = (attachment.fileName, attachment.data, 'application/octet-stream')

        url = f"{self.url}{RECORD_INSTANCE_PATH}"
        response = self.session.post(url=url, files=multipart_form_data, headers=connector.headers_basic)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (f"Failed to create record instance using FormData : {record_instance},  "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        location = response.headers['Location']
        record_id = location.split("/")[-1]
        return record_id

    def delete_record_instance(self, record_definition_name, guid):
        url = f"{self.url}{RECORD_INSTANCE_PATH}/{record_definition_name}/{guid}"
        response = self.session.delete(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.NO_CONTENT:
            error_message = (f"Failed to delete record instance, recordDefinitionName : {record_definition_name}, "
                             f"guid : {guid}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)

    def get_record_definition(self, record_definition_name):
        url = f"{self.url}{RECORD_DEFINITION_PATH}/{record_definition_name}"
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get record definition : {record_definition_name},  "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_record_definitions_details(self, bundle_scope, **kwargs):
        page_size = kwargs.get('pageSize', -1)
        start_index = kwargs.get('startIndex', 0)
        request_overlay_group = kwargs.get('request_overlay_group', "1")
        property_selections = "name,lastUpdateTime,lastChangedBy,customizationPerspective,recordDefinitionType,overlayGroupId,overlayDescriptor,isAuditRecordDefinition,scope,externalDataSourceType,archiveSourceRecordDefinitionName,type"
        url = f"{self.url}{PATH_OF_RX_APP_DATAPAGE}?dataPageType={RECORD_INSTANCE_DATA_PAGE_QUERY}&startIndex={start_index}&pageSize={page_size}&propertySelection={property_selections}"
        connector.headers[DEFAULT_BUNDLE_SCOPE] = bundle_scope
        connector.headers[REQUEST_OVERLAY_GROUP] = request_overlay_group
        response = self.session.get(url=url, headers=connector.headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (
                f"Failed to make record definition dataPage query for bundleScope: {bundle_scope},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        json_response = json.loads(response.content)
        return json_response

    def copy_record_definition(self, src_name, dest_name, **kwargs):
        return self.copy_definition_service.copy_workflow_definition("RECORD_DEFINITION", src_name, dest_name, **kwargs)
