import json
from urllib.parse import urlencode
from utils import logger
from requests import status_codes

from commons import connector
from dwpc.constants import SERVICE_REQUEST_PATH, SR_EXTENDED_SEARCH_PATH

_LOGGER = logger.get_logger(__name__)


class ServiceCatalogService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def submit_request(self, service_id, request_id):
        url = f"{self.url}/api/myit-sb/services/{service_id}/requests/{request_id}/submissions"
        response = self.session.post(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (f"Failed to submit SR {request_id}"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def create_service_request(self, service_id):
        payload = {"serviceId": service_id}
        url = f"{self.url}{SERVICE_REQUEST_PATH}"
        response = self.session.post(url=url, data=json.dumps(payload), headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (f"Failed to create service request"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def search_service_requests(self, **kwargs):
        query_params = {}
        query_params['currentUserSubCatalogOnly'] = kwargs.get('currentUserSubCatalogOnly', "true")
        query_params['includeCanRestartProcessInstance'] = kwargs.get('includeCanRestartProcessInstance', "true")
        query_params['page'] = kwargs.get('page', "1")
        query_params['perPage'] = kwargs.get('perPage', "20")
        query_params['sortBy'] = kwargs.get('sortBy', "status.startTime")
        query_params['sortDirection'] = kwargs.get('sortDirection', "desc")
        if 'submittedDateFrom' in kwargs:
            query_params['submittedDateFrom'] = kwargs['submittedDateFrom']
        if 'submittedDateTo' in kwargs:
            query_params['submittedDateTo'] = kwargs['submittedDateTo']
        if 'search' in kwargs:
            query_params['search'] = kwargs['search']
        if 'status' in kwargs:
            query_params['status'] = kwargs['status']
        if 'companyId' in kwargs:
            query_params['companyId'] = kwargs['companyId']
        encoded_query_params = urlencode(query_params)
        url = f"{self.url}{SR_EXTENDED_SEARCH_PATH}?{encoded_query_params}"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to perform extended requests search"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
