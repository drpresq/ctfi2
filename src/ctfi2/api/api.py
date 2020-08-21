import os
from requests import Session, Response
from requests.exceptions import BaseHTTPError as RequestErr
from json import dumps
from csv import DictReader

from ctfi2.api.constants import err_msg, dat, check_fields, check_response, check_output_types


class API(Session):

    def __init__(self, prefix_url: str = None, user: str = None, passwd: str = None, api_key: str = None) -> None:
        super(API, self).__init__()
        self.prefix_url: str = prefix_url
        self.api_key: str = api_key
        if user and passwd:
            self.login(user, passwd)

    def request(self, method, url, *args, **kwargs) -> Response:
        url = "{}/{}".format(self.prefix_url, url)
        return super(API, self).request(method, url, *args, **kwargs)

    # Authentication Functions

    def login(self, name: str, password: str) -> bool:
        data = {'name': name, 'password': password, 'nonce': self._get_nonce("login")}
        head = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.post("login", data, head)
        except RequestErr as e:
            raise Exception(err_msg.format('Login', e))
        return True if 'challenges' in response.url else False

    def logout(self) -> bool:
        try:
            response = self.get("logout")
        except RequestErr as e:
            raise Exception(err_msg.format('Logout', e))
        return check_response(response, **{'status': True, 'url': self.prefix_url})

    # Server Initialize and Reset Functions

    def server_init(self, data: dict) -> bool:
        """Initializes the server using the provided data.
        Minimum data fields are:
            ctf_name, ctf_description, user_mode, name, email and password"""
        page = "setup"
        data.update({"nonce": self._get_nonce(page)})

        return True if "{}/".format(self.prefix_url) == self.post(page, data=data).url else False

    def server_reset(self, data: dict) -> bool:
        """Wipes the server of all data: Users, Subissions, Challenges, Pages and Notifications."""
        page = "admin/reset"
        head = {"Content-Type": "application/x-www-form-urlencoded"}
        data.update({"nonce": self._get_nonce()})
        return True if 'setup' in self.post(page, data=data, headers=head).url else False

    ##
    #   Private Server Interaction Functions
    ##

    def _get_nonce(self, page: str = None) -> str:
        nonce_url = "admin/reset" if not page else page
        try:
            response = self.get(nonce_url).text.splitlines()
        except RequestErr as e:
            raise Exception(err_msg.format('Get Nonce', e))
        return [line for line in response if "csrf" in line][0].split('"')[1]

    def _get_obj(self, obj: str, obj_id: int = None) -> list:
        got_obj: list = []
        page: str = dat[obj]['url']['single'].format(obj_id) if obj_id else dat[obj]['url']['all']
        try:
            response = self.get(page)
            if check_response(response, **{'status': True, 'json': True}):
                got_obj.append(response.json()['data'])
        except RequestErr as e:
            raise Exception(err_msg.format("Get Object", e))
        return got_obj

    def _get_csv(self, obj: str) -> list:
        ret_list: list = []
        page: str = 'admin/export/csv?table={}'.format(obj)
        try:
            response = self.get(page)
        except RequestErr as e:
            raise Exception(err_msg.format('Get CSV', e))
        if check_response(response, **{'status': True}):
            dictreader = DictReader(response.text.split('\r\n'))
            for row in dictreader:
                ret_list.append(row)
        return ret_list

    @check_fields
    def _add_obj(self, obj: str, **kwargs) -> dict:
        files = {}
        new_obj = {}

        if obj != 'files':
            try:
                head = {"CSRF-Token": self._get_nonce(), "Content-Type": "application/json"}
                data: dict = kwargs
                data.pop('id') if 'id' in data.keys() else None
                data: str = dumps(data, separators=(",", ":"))
            except Exception as e:
                raise e

        elif obj == 'files':
            head = {}
            data = kwargs['data']
            files = kwargs['files']
            kwargs.pop('files')

        try:
            response = self.post(dat[obj]['url']['all'],
                                 files=files,
                                 data=data,
                                 headers=head)
            if check_response(response, **{"status": True, "json": True}):
                new_obj = response.json()['data']
        except RequestErr as e:
            raise Exception(err_msg.format('Add Object', e))
        except Exception as e:
            raise Exception(err_msg.format('Add Objects', '{}\n\t{}'.format(data, e)))

        return new_obj

    @check_fields
    def _update_obj(self, obj: str, **kwargs) -> dict:
        update_obj: dict = {}
        head = {"Content-Type": "application/json", "CSRF-Token": self._get_nonce()}
        try:
            data: dict = kwargs
            response = self.patch(dat[obj]['url']['single'].format(kwargs['id']),
                                  data=dumps(data, separators=(",", ":")),
                                  headers=head)
            if check_response(response, **{'status': True, 'json': True}):
                update_obj = response.json()['data']
        except KeyError as e:
            raise Exception(err_msg.format('Update Object', e))
        except RequestErr as e:
            raise Exception(err_msg.format('Update Object', e))

        return update_obj

    @check_fields
    def _delete_obj(self, obj: str, **kwargs) -> bool:
        try:
            obj_id = kwargs['id']
            head = {"Content-Type": "application/json", "CSRF-Token": self._get_nonce()}
            response = self.delete(dat[obj]['url']['single'].format(obj_id), headers=head)
        except KeyError as e:
            raise Exception(err_msg.format("Delete", e))
        except RequestErr as e:
            raise Exception(err_msg.format("Delete", e))

        return check_response(response, **{"status": True})

    ##
    #   Private Data Paring Functions
    ##

    @check_fields
    def _find_obj(self, obj: str, **kwargs) -> list:
        try:
            objs: list = self._get_obj(obj)
        except Exception as e:
            raise e
        if isinstance(objs, list):
            print(objs)
            for key in kwargs:
                obj = [item for item in objs if item[key] == kwargs[key]]
        elif isinstance(objs, dict):
            obj = [objs]
        return obj

    # User Functions
    @check_output_types
    def user_csv(self) -> list:
        user_csv: list = [user for user in self._get_csv('users') if user['type'] != 'admin']
        return user_csv

    @check_output_types
    def user_get(self, user_id: int) -> dict:
        return next((user for user in self._get_obj('users', user_id)))

    @check_output_types
    def user_add(self, **kwargs) -> dict:
        new_user: dict = self._add_obj('users', **kwargs)
        if 'password' in new_user.keys():
            new_user.pop('password')
        return new_user

    @check_output_types
    def user_update(self, **kwargs) -> dict:
        update_user: dict = self._update_obj('users', **kwargs)
        if 'password' in update_user.keys():
            update_user.pop('password')
        return update_user

    def user_delete(self, **kwargs) -> bool:
        return self._delete_obj('users', **kwargs)

    # Challenge Functions

    @check_output_types
    def challenge_csv(self) -> list:
        return self._get_csv(obj='challenges')

    @check_output_types
    def challenge_get(self, challenge_id: int) -> dict:
        return next(self._get_obj('challenges', challenge_id))

    @check_output_types
    def challenge_add(self, **kwargs) -> dict:
        return self._add_obj('challenges', **kwargs)

    @check_output_types
    def challenge_update(self, **kwargs) -> dict:
        return self._update_obj('challenges', **kwargs)

    def challenge_delete(self, **kwargs) -> bool:
        return self._delete_obj('challenges', **kwargs)

    # Flag Functions

    @check_output_types
    def flag_csv(self) -> list:
        return self._get_csv(obj='flags')

    @check_output_types
    def flag_get(self, flag_id: int = None) -> dict:
        return next(self._get_obj('flags', flag_id))

    @check_output_types
    def flag_add(self, **kwargs) -> dict:
        print("flag_add - in: {}".format(kwargs))
        return self._add_obj('flags', **kwargs)

    @check_output_types
    def flag_update(self, **kwargs) -> dict:
        return self._update_obj('flags', **kwargs)

    def flag_delete(self, **kwargs) -> bool:
        return self._delete_obj('flags', **kwargs)

    # Hint Functions

    @check_output_types
    def hint_csv(self) -> list:
        return self._get_csv(obj='hints')

    @check_output_types
    def hint_get(self, hint_id: int) -> dict:
        return next(self._get_obj('hints', hint_id))

    @check_output_types
    def hint_add(self, **kwargs) -> dict:
        return self._add_obj('hints', **kwargs)

    @check_output_types
    def hint_update(self, **kwargs) -> dict:
        return self._update_obj('hints', **kwargs)

    def hint_delete(self, **kwargs) -> bool:
        return self._delete_obj('hints', **kwargs)

    # File Functions

    @check_output_types
    def file_get(self, file_id: int = None) -> list:
        files: list = []
        if not file_id:
            challenges: list = self.challenge_csv()
            challenges = [item['id'] for item in challenges]
            for obj_id in challenges:
                for file in self.get('api/v1/challenges/{}/files'.format(obj_id)).json()['data']:
                    file.update({'challenge_id': obj_id})
                    files.append(file)
        return files

    @check_output_types
    def file_add(self, **kwargs) -> dict:
        name = kwargs['path'].split('/')[-1]
        kwargs = {'files': {"file": (name, open(kwargs['path'], 'rb'))},
                  'data': {'nonce': self._get_nonce(), 'challenge': int(kwargs['challenge']), 'type': 'challenge'}}
        return self._add_obj('files', **kwargs)

    def file_delete(self, **kwargs) -> bool:
        if 'path' in kwargs and os.path.exists(kwargs['path']):
            os.system('/bin/rm -rf {}'.format(kwargs['path']))
        return self._delete_obj('files', **kwargs)
