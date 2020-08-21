import os
from re import match
from functools import wraps
from requests import Response
from simplejson.errors import JSONDecodeError

TITLE = 'CTFi2'
AUTHOR = 'George'
VERSION = '1.5 (Acceptable Axolotl)'

pattern_email = r"[a-zA-Z0-9_-]*@[a-zA-Z0-9]*\.[a-zA-Z]{2,3}"
pattern_hash = r'.*,(\"\$bcrypt.*\"),.*'

FILE_PATH = os.path.join(os.path.expanduser("~"), ".ctfi2")

err_msg = "API Error:\n\tMethod: {}\n\tData: {}"

url_api: str = "api/v1/{}"

dat: dict = {'users': {'url': {'all': url_api.format("users"),
                               'single': url_api.format("users/{}")},
                       'kwargs': {'valid': ["name", "email", "password", "website", "affiliation",
                                            "country", "type", "verified", "hidden", "banned", 'id'],
                                  'minimum': ["name", "email", "type", "verified", "hidden", "banned"],
                                  'search': ['name', 'email', 'id'],
                                  'delete': ['id']}
                       },
             'challenges': {'url': {'all': url_api.format("challenges"),
                                    'single': url_api.format("challenges/{}")},
                            'kwargs': {'valid': ['name', 'category', 'description', 'value', 'state', 'type', 'id', 'requirements'],
                                       'minimum': ['name', 'category', 'description', 'value', 'state', 'type'],
                                       'search': ['name', 'id'],
                                       'delete': ['id']},
                            },
             'flags': {'url': {'all': url_api.format("flags"),
                               'single': url_api.format("flags/{}")},
                       'kwargs': {'valid': ['challenge_id', 'content', 'id', 'data', 'challenge', 'type'],
                                  'minimum': ['challenge_id', 'content', 'data', 'type'],
                                  'search': ['challenge_id', 'id'],
                                  'delete': ['id']}
                       },
             'hints': {'url': {'all': url_api.format("hints"),
                               'single': url_api.format("hints/{}")},
                       'kwargs': {'valid': ['content', 'cost', 'challenge', 'id'],
                                  'minimum': ['content', 'cost'],
                                  'search': ['id'],
                                  'delete': ['id']}
                       },
             'files': {'url': {'all': url_api.format("files"),
                               'single': url_api.format("files/{}")},
                       'kwargs': {'valid': ['location', 'id', 'type', 'challenge', 'path', 'challenge_id'],
                                  'minimum': ['challenge', 'type'],
                                  'search': ['id'],
                                  'delete': ['id']}
                       }
             }


def check_response(response: Response, **kwargs):
    ret: bool = False
    if 'status' in kwargs:
        ret = True if response.status_code == 200 else False
    if 'json' in kwargs:
        try:
            ret = True if response.json()['success'] else False
        except JSONDecodeError:
            ret = False
        except KeyError as e:
            raise Exception(err_msg.format("Check Response", ('{}\n\t{}\n\t{}'.format('Json', e, response.json()))))
    if 'url' in kwargs:
        ret = True if kwargs['url'] in response.url else False

    return ret


def check_fields(function):
    @wraps(function)
    def field_wrapper(*args, **kwargs):
        obj = args[1]
        filters = 'delete' if 'delete' in function.__name__ else 'minimum'
        if obj != 'files' and obj != 'server':

            missing_args = [item for item in dat[obj]['kwargs'][filters] if item not in kwargs.keys()] or None
            if missing_args:
                raise Exception(err_msg.format(obj, missing_args))

            kwargs = {key: value for key, value in kwargs.items() if key in dat[obj]['kwargs']['valid']}
            if 'password' in kwargs.keys() and match('\\"\\$bcrypt.*\\"', kwargs['password']):
                kwargs.pop('password')
            if 'add' in function.__name__ and 'id' in kwargs.keys():
                kwargs.pop('id')

        return function(*args, **kwargs)

    return field_wrapper


def check_output_types(function):
    @wraps(function)
    def type_wrapper(*args, **kwargs):
        data_obj = function(*args, **kwargs)
        if isinstance(data_obj, dict):
            data_obj: list = [data_obj]
        for obj in data_obj:
            for key in obj.keys():
                # str
                if key in ['name', 'email', 'password', 'website', 'country', 'content',
                           'type', 'category', 'description', 'location', 'state']:
                    if not isinstance(obj[key], str) and obj[key]:
                        try:
                            obj[key] = str(obj[key])
                        except ValueError:
                            obj[key] = ''
                # bool
                if key in ["verified", "hidden", "banned"]:
                    if not isinstance(obj[key], bool) and obj[key]:
                        try:
                            obj[key] = True if obj[key] == 'True' else False
                        except ValueError:
                            obj[key] = False
                # int
                if key in ['value', 'id', 'challenge_id', 'challenge', 'cost']:
                    if not isinstance(obj[key], int) and obj[key]:
                        try:
                            obj[key] = int(obj[key])
                        except ValueError:
                            obj[key] = None

        if 'get' in function.__name__ or 'csv' in function.__name__:
            pass
        else:
            data_obj: dict = data_obj[0]

        return data_obj

    return type_wrapper
