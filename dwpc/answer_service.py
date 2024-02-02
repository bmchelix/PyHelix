import json
from utils import logger

from requests import status_codes
from commons import connector

_LOGGER = logger.get_logger(__name__)


class AnswerService:

    def __init__(self, connection):
        self.session = connection.getSession()
        self.url = connection.getUrl()

    def submit_service_request_answer(self, **kwargs):
        service_id = kwargs['serviceId']
        questionnaire_id = kwargs['questionnaireId']
        question_id = kwargs['questionId']
        answer = kwargs['answer']
        request_id = kwargs['requestId']
        payload = {
            "questionnaireId": questionnaire_id,
            "questionId": question_id,
            "answers": [answer],
            "serviceRequestId": request_id
        }
        url = f"{self.url}/api/myit-sb/services/{service_id}/questionnaire/answers"
        response = self.session.post(url=url, data=json.dumps(payload), headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to send answer to a question"
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result

    def get_request_answers(self, request_id):
        url = f"{self.url}/api/myit-sb/services/requests/{request_id}/answers"
        response = self.session.get(url=url, headers=connector.dwpc_headers)
        if response.status_code != status_codes.codes.OK:
            error_message = (f"Failed to get answers for request Id : {request_id}, "
                             f"response code : {response.status_code} , body : {response.content}")
            _LOGGER.error(error_message)
            raise Exception(error_message)
        result = json.loads(response.content)
        return result
