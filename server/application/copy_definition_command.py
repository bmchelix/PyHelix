import json

from requests import status_codes
from utils import logger
from commons import connector

from server.constants import PATH_OF_RX_APP_COMMAND, REQUEST_OVERLAY_GROUP

_LOGGER = logger.get_logger(__name__)


class CopyDefinitionServiceImpl:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def copy_workflow_definition(self, def_type, src_name, dest_name, **kwargs):
        url = f"{self.url}{PATH_OF_RX_APP_COMMAND}"
        body_request = {}
        bundle_scope = kwargs.get('bundleScope', None)
        if bundle_scope:
            body_request['bundleScope'] = bundle_scope
        body_request['srcName'] = src_name
        body_request['destName'] = dest_name
        body_request['resourceType'] = "com.bmc.arsys.rx.application.common.CopyDefinitionCommand"
        body_request['type'] = def_type
        connector.headers[REQUEST_OVERLAY_GROUP] = "1"
        response = self.session.post(url=url, data=json.dumps(body_request), headers=connector.headers)
        if response.status_code != status_codes.codes.CREATED:
            error_message = (
                f"Failed to execute {def_type} definition copy command,  srcName = {src_name} , destName = {dest_name},  "
                f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        return response.headers['Location']
