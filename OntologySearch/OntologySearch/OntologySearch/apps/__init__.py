# conding: UTF-8
import logging, decimal, json
from django.http import HttpResponse

_logger = logging.getLogger(__name__)

class JSONDecimalEncoder (json.JSONEncoder):
    def default (self, obj):
        data = obj
        if isinstance(obj, decimal.Decimal):
            return float(str(obj))
        return super(JSONDecimalEncoder, self).default(data)

def _response (request, status, payload={}, msg='', encoder=json.JSONEncoder):
    response = HttpResponse(json.dumps({
        'header': {
            'status': status,
            'message' : msg,
        },
        'payload': payload,
    }, cls=encoder), status=status, content_type='application/json; charset=utf-8')
    response['Pragram'] = 'no-cache'
    return response

def response_success (request, payload={}, msg='Success', encoder=json.JSONEncoder):
    return _response (request, 200, payload, msg, encoder)

def response_successCORS (request, payload={}, msg='Success', encoder=json.JSONEncoder):
    res = _response (request, 200, payload, msg, encoder)
    res["Access-Control-Allow-Origin"] = "*"
    return res


def response_badrequest (request, payload={}, msg='Bad Request', encoder=json.JSONEncoder):
    return _response (request, 400, payload, msg, encoder)

def response_unauthorized (request, payload={}, msg='Unauthorized', encoder=json.JSONEncoder):
    return _response (request, 401, payload, msg, encoder)

def response_forbidden (request, payload={}, msg='Forbidden', encoder=json.JSONEncoder):
    return _response (request, 403, payload, msg, encoder)

def response_notfound (request, payload={}, msg='Page not found', encoder=json.JSONEncoder):
    return _response (request, 404, payload, msg, encoder)

def response_notallowed (request, payload={}, msg='Method Not Allowed', encoder=json.JSONEncoder):
    return _response (request, 405, payload, msg, encoder)

def response_internal_server_error (request, payload={}, msg='Internal Server Error', encoder=json.JSONEncoder):
    return _response (request, 500, payload, msg, encoder)
