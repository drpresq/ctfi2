import os

from ctfi2.api import API, dat, FILE_PATH, check_fields


class Configuration:
    # Admin Credentials
    admin_token: {str: str} = {"Authorization": "Token {}"}

    # Default Challenge Configuration
    configuration: dict = {"server": {'url_prefix': "http://localhost:8000",
                                      'ctf_name': "CTFd",
                                      'ctf_description': "This Competition was generated with the CTFi2!",
                                      'user_mode': "users",
                                      'name': "root",
                                      'email': "root@ctfd.io",
                                      'password': "toor",
                                      'ctf_theme': "core",
                                      'theme_color': '',
                                      'start': '1610694000',
                                      'end': '1610694000',
                                      'freeze': "1610694000",
                                      'score_visibility': "public",
                                      'account_visibility': "public"
                                      },
                           "challenges": [],
                           "flags": [],
                           "hints": [],
                           "files": [],
                           "requirements": [],
                           "users": []
                           }
    # Default Email Settings (Unused)
    email: dict = {"email": {'verify_emails': "0",
                             'mail_server': '',
                             'mail_port': '',
                             'mail_tls': '0',
                             'mail_ssl': '0',
                             'mail_username': '',
                             'mail_password': '',
                             'mail_useauth': '',
                             'verification_email_subject': "Confirm your account for {ctf_name}",
                             'verification_email_body': "Please click the following link to confirm "
                                                        "your email address for {ctf_name}: {url}",
                             'successful_registration_email_subject': "Successfully registered for "
                                                                      "{ctf_name}",
                             'successful_registration_email_body': "You've successfully registered "
                                                                   "for {ctf_name}!",
                             'user_creation_email_subject': "Message from {ctf_name}",
                             'user_creation_email_body': "An account has been created for you for {"
                                                         "ctf_name} at {url}.\n\nUsername: {"
                                                         "name}\nPassword: {password}",
                             'password_reset_subject': "Password Reset Request from {ctf_name}",
                             'password_reset_body': "Did you initiate a password reset? If you "
                                                    "didn't initiate this request you can ignore "
                                                    "this email. \n\nClick the following link to "
                                                    "reset your password:\n{url}",
                             'password_change_alert_subject': "Password Change Confirmation for {"
                                                              "ctf_name}",
                             'password_change_alert_body': "Your password for {ctf_name} has been "
                                                           "changed.\n\nIf you didn't request a "
                                                           "password change you can reset your "
                                                           "password here: {url} "
                             }
                   }
    # API Vars
    api_session: API = None

    ###
    #       Data Interface
    ###

    def read(self, obj: str, obj_id: int = None) -> dict:
        if obj != 'server' and obj not in dat.keys():
            raise Exception("{}: Expected one of the following: {}".format(obj, list(dat.keys())))
        ret_obj: dict = self.configuration[obj] if obj == 'server' \
            else next((item for item in self.configuration[obj] if int(item['id']) == int(obj_id)), {})
        if not ret_obj:
            raise Exception("Read Failed: configuration item not found: {}:{}".format(obj, obj_id))

        return ret_obj

    @check_fields
    def update(self, obj: str, **kwargs) -> None:
        if obj != 'server' and obj not in dat.keys():
            raise Exception("{}: Expected one of the following: {}".format(obj, list(dat.keys())))

        if obj == 'server':
            self.configuration[obj].update(kwargs)
        else:
            obj_index: int = next((self.configuration[obj].index(item) for item in self.configuration[obj]
                                   if item['id'] == kwargs['id']), -1)

            if obj_index >= 0:
                self.configuration[obj][obj_index].update(kwargs)
            else:
                raise Exception("Update Failed: configuration item not found: {}:{}".format(obj, obj_index))

    @check_fields
    def add(self, obj: str, **kwargs) -> None:
        api_funcs: dict = {'challenges': self.challenge_api,
                           'flags': self.flag_api,
                           'hints': self.hint_api,
                           'files': self.file_api,
                           'users': self.user_api}
        if obj not in api_funcs.keys():
            raise Exception("{}: Expected one of the following: {}".format(obj, list(api_funcs.keys())))

        # # Our ID generator values must be initialized as they are not persistent between runs
        kwargs.update({'id': 0})
        if len(self.configuration[obj]) > 0:
            kwargs.update({'id': self.next_id(obj)})

        # Update Object Remote and Locally
        api_funcs[obj]('new', kwargs)

    def remove(self, obj: str, obj_id: int):
        api_funcs: dict = {'challenges': self.challenge_api,
                           'flags': self.flag_api,
                           'hints': self.hint_api,
                           'files': self.file_api,
                           'users': self.user_api}
        if obj not in dat.keys() or obj == 'server':
            keys = dat
            _ = keys.pop('server')
            raise Exception("{}: Expected one of the following: {}".format(obj, list(keys.keys())))
        obj_dat = next((self.configuration[obj].pop(index)
                        for index, item in enumerate(self.configuration[obj])
                        if int(item['id']) == int(obj_id)), {})
        if obj_dat:
            api_funcs[obj](action='delete', obj=obj_dat)
        else:
            raise Exception("Delete Failed: configuration item not found: {}:{}".format(obj, obj_id))

    def next_id(self, obj: str) -> int:
        return max([item['id'] for item in self.configuration[obj]]) + 1 \
            if [item['id'] for item in self.configuration[obj]] else 0

    ###
    #       Private CTFd API Interaction Functions
    ###

    def _api_isAuthenticated(self) -> bool:
        try:
            if not self.api_session:
                self.api_session = API(prefix_url=self.configuration['server']['url_prefix'])

            self.api_session.login(name=self.configuration['server']['name'],
                                   password=self.configuration['server']['password'])
            return True
        except:
            return False

    def _api_alterConfig(self, action: str, obj: str, obj_item: dict = None):
        if self._api_isAuthenticated():
            actions: dict = {'users': {'get': self.api_session.user_get,
                                       'new': self.api_session.user_add,
                                       'update': self.api_session.user_update,
                                       'delete': self.api_session.user_delete,
                                       'csv': self.api_session.user_csv},
                             'challenges': {'get': self.api_session.challenge_get,
                                            'new': self.api_session.challenge_add,
                                            'update': self.api_session.challenge_update,
                                            'delete': self.api_session.challenge_delete,
                                            'csv': self.api_session.challenge_csv},
                             'flags': {'get': self.api_session.flag_get,
                                       'new': self.api_session.flag_add,
                                       'update': self.api_session.flag_update,
                                       'delete': self.api_session.flag_delete,
                                       'csv': self.api_session.flag_csv},
                             'hints': {'get': self.api_session.hint_get,
                                       'new': self.api_session.hint_add,
                                       'update': self.api_session.hint_update,
                                       'delete': self.api_session.hint_delete,
                                       'csv': self.api_session.hint_csv},
                             'files': {'new': self.api_session.file_add,
                                       'delete': self.api_session.file_delete,
                                       'csv': self.api_session.file_get}
                             }

            if action in actions[obj].keys():
                result = actions[obj][action](**obj_item)
                if isinstance(result, dict):
                    obj_item.update(result)
                    self.configuration[obj].append(obj_item)

            elif action == 'sync':

                objs_remote = actions[obj]['csv']()
                objs_local = self.configuration[obj]
                objs_delta: list = []

                for index, local_obj in enumerate(objs_local):
                    found: bool = False
                    # Match local object IDs to remote object IDs
                    for remote_obj in objs_remote:
                        # Update objects that use the name field
                        if ('id' in remote_obj.keys() and remote_obj['id'] == local_obj['id']) and (
                                'name' in remote_obj.keys() and remote_obj['name'] == local_obj['name']):
                            local_obj.update({'id': remote_obj['id']})
                            local_obj = actions[obj]['update'](**local_obj)
                            self.update(obj, **local_obj)
                            _ = objs_remote.pop(objs_remote.index(remote_obj))
                            found = True
                            break
                        elif 'name' in remote_obj.keys() and remote_obj['name'] == local_obj['name']:
                            local_obj.update({'id': remote_obj['id']})
                            local_obj = actions[obj]['update'](**local_obj)
                            self.update(obj, **local_obj)
                            _ = objs_remote.pop(objs_remote.index(remote_obj))
                            found = True
                            break
                        # Update objects that use the content field
                        elif 'content' in remote_obj.keys() and remote_obj['content'] == local_obj['content']:
                            local_obj.update({'id': remote_obj['id']})
                            self.update(obj, **local_obj)
                            _ = objs_remote.pop(objs_remote.index(remote_obj))
                            found = True
                            break
                        # Update objects that use the location field
                        elif 'location' in remote_obj.keys() \
                                and remote_obj['location'].split('/')[-1] == local_obj['path'].split('/')[-1] \
                                and remote_obj['challenge_id'] == local_obj['challenge_id']:
                            local_obj.update({'id': remote_obj['id'], 'location': remote_obj['location']})
                            self.update(obj, **local_obj)
                            _ = objs_remote.pop(objs_remote.index(remote_obj))
                            found = True
                            break
                    if not found:
                        objs_delta.append(local_obj)

                # Add new remote objects to local config
                for remote_obj in objs_remote:
                    self.configuration[obj].append(remote_obj)

                # Add new local objects to remote config
                for obj_item in objs_delta:
                    response = actions[obj]['new'](**obj_item)
                    self.configuration[obj][self.configuration[obj].index(obj_item)].update(response)
        else:
            if action == 'new':
                self.configuration[obj].append(obj_item)

    def _api_downloadFiles(self, location: str, path: str) -> str:
        file_name = location.split("/")[-1]
        if not os.path.exists(path):
            os.mkdir(path)
        with open("{}/{}".format(path, file_name), "wb") as file:
            file.write(self.api_session.get("files/{}".format(location)).content)
        return "{}/{}".format(path, file_name) if os.path.exists("{}/{}".format(path, file_name)) else ''

    ##
    #   Public Facing CTFd API Interaction Functions
    ##

    def challenge_api(self, action: str, obj: dict = None) -> None:
        challenge_id = obj['id'] if obj else None
        self._api_alterConfig(action=action, obj='challenges', obj_item=obj)
        # Sync all challenge related objects
        if action == 'sync':
            for section in ['flags', 'hints', 'files']:
                self._api_alterConfig(action='sync', obj=section)

            for file in self.configuration['files']:
                folder_path = "{}{}".format(FILE_PATH, next(item['name']
                                                            for item in self.configuration['challenges']
                                                            if item['id'] == file['challenge_id']))
                if 'path' not in file.keys():
                    file['path'] = ''
                if file['location'] and file['path'] == '':
                    full_path: str = self._api_downloadFiles(location=file['location'], path=folder_path)
                    next(item for item in self.configuration['files']
                         if item['id'] == file['id']).update({'path': full_path})

        if action == 'delete':
            flags: list = [flag for flag in self.configuration['flags'] if flag['challenge_id'] == challenge_id] or []
            if flags:
                for flag in flags:
                    self.flag_api(action='delete', obj=flag)
            hints: list = [hint for hint in self.configuration['hints'] if hint['challenge_id'] == challenge_id] or []
            if hints:
                for hint in hints:
                    self.hint_api(action='delete', obj=hint)
            files: list = [item for item in self.configuration['files'] if item['challenge_id'] == challenge_id] or []
            if files:
                for file in files:
                    if os.path.exists(file['path']):
                        os.system('/bin/rm -rf {}'.format('/'.join(file['path'].split('/')[:-1])))
                    self.file_api(action='delete', obj=file)

    def flag_api(self, action: str, obj: dict) -> None:
        self._api_alterConfig(action=action, obj='flags', obj_item=obj)

    def hint_api(self, action: str, obj: dict) -> None:
        self._api_alterConfig(action=action, obj='hints', obj_item=obj)

    def file_api(self, action: str, obj: dict) -> None:
        if action == 'delete':
            if os.path.exists(obj['path']):
                os.system('/bin/rm {}'.format(obj['path']))
        self._api_alterConfig(action=action, obj='files', obj_item=obj)

    def user_api(self, action: str, obj: dict = None) -> None:
        self._api_alterConfig(action=action, obj='users', obj_item=obj)

    def server_check(self, **kwargs) -> bool:
        """Checks if server live and if it needs initialized, wiped or reset"""
        # TODO: The return behavior is crushingly trivial and provides terrible coverage but ... /shrug for now
        COMPLETE = True
        PROMPT_WIPE = False
        self.configuration['server'].update(kwargs)
        self.api_session = API(prefix_url=kwargs['url_prefix'])
        # If uninitialized go ahead and do it
        if "setup" in self.api_session.get('/').url:
            data: dict = {key: value for key, value in self.configuration['server'].items() if key != 'url_prefix'}
            self.api_session.server_init(data)
            return COMPLETE
        elif "{}/".format(kwargs['url_prefix']) == self.api_session.get('/').url:
            return PROMPT_WIPE

    def server_wipe(self) -> bool:
        """Wipes the server: Deletes all users, challenges, challenge files, hints, flags, and statistics"""
        if self._api_isAuthenticated():
            data: dict = {"accounts": "y",
                          "submissions": "y",
                          "challenges": "y",
                          "pages": "y",
                          "notifications": "y"}
            if self.api_session.server_reset(data):
                data: dict = {key: value for key, value in self.configuration['server'].items() if key != 'url_prefix'}
                return self.api_session.server_init(data)
        return False

    def server_reset(self) -> bool:
        """Resets the server: Deletes all users and statistics"""
        if self._api_isAuthenticated():
            data: dict = {"accounts": "y",
                          "submissions": "y",
                          "notifications": "y"}
            if self.api_session.server_reset(data):
                data: dict = {key: value for key, value in self.configuration['server'].items() if key != 'url_prefix'}
                return self.api_session.server_init(data)
        return False
