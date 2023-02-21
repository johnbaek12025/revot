import json
from main.models.client import State


class BaseJsonFormat:

    def __init__(self, *, msg=None, is_success=True, error_msg=None, data: list = None):
        self.is_success = is_success
        self.msg = msg
        self.error_msg = error_msg
        self.data = data        

    def __str__(self):

        return json.dumps(self.__dict__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_state_from(state_n=0):
    try:
        s = State.objects.get(state=state_n)
    except State.DoesNotExist:
        s = State(state=state_n)
        s.save()
    return s