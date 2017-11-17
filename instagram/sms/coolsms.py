from django.conf import settings
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_sms(receiver, message):
    api_key = settings.COOLSMS_API_KEY
    api_secret = settings.COOLSMS_API_SECRET
    sender = settings.COOLSMS_SENDER

    params = dict()
    params['type'] = 'sms'
    params['to'] = receiver
    params['from'] = sender
    params['text'] = message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        data = {
            'success_count': response['success_count'],
            'error_count': response['error_count'],
            'error_list': response.get('error_list', []),
        }
        return data
    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
