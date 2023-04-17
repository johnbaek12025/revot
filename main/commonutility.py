import json
from main.models.client import State
import os
from datetime import datetime, timedelta
from random import randrange


class BaseJsonFormat:

    def __init__(self, *, msg=None, is_success=True, error_msg=None, data: list = None, data_count = 0):
        self.is_success = is_success
        self.msg = msg
        self.error_msg = error_msg
        self.data = data
        if data_count != 0:
            self.data_count = data_count

    def __str__(self):
        return json.dumps(self.__dict__, default=str)


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

def save_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str(data))
        
        
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)    
    return start + timedelta(seconds=random_second)

def to_bool(x):
    if x is None:
        return None
    if isinstance(x, str) and x.lower() == 'none':
        return None
    try:
        if x.lower() in ['true', 'yes', 't']:            
            return True
        elif x.lower() in ['false', 'no', 'f']:
            return False
    except AttributeError:
        
        pass
    try:
        return bool(int(x))
    except (ValueError, TypeError):
        pass
    raise ValueError("Unknown boolean specifier: '%s'." % x)