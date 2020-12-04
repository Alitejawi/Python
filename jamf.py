#!/usr/bin/env python3

__author__ = "Shane Young"
__version__ = "1.1"
__email__ = "thedzy@hotmail.com"

import requests
import urllib3


class APIResponse:
    """
    Data object containing data of the query
    :property success: (bool) success of the call
    :property url: (str) url that was called
    :property response: (str, json) depending on the success
    :property http_code: (int) http code returned
    :property err: (str) Error if exception
    """

    def __init__(self, success=False, url=None, response=None, http_code=0, err=None, **kwargs):
        """
        Initialisation method
        :param success: (bool) success of the call
        :param url: (str) url that was called
        :param response: (str, json) depending on the success
        :param http_code: (int) http code returned
        :param err: (str) Error if exception
        :param kwargs: (dict)
        """
        self.success = kwargs['success'] if 'success' in kwargs else success
        self.url = kwargs['url'] if 'url' in kwargs else url
        self.response = kwargs['response'] if 'response' in kwargs else response
        self.http_code = kwargs['http_code'] if 'http_code' in kwargs else http_code
        self.err = kwargs['err'] if 'err' in kwargs else err

        self.data = self.response

    def success(self, success=None):
        """
        :param success: Set or retrieve property success
        :return: (bool) Current/new setting
        """
        if success is not None:
            self.success = bool(success)

        return self.success

    def response(self, response=None):
        """
        :param response: Set or retrieve property response
        :return: (int) Current/new setting
        """
        if response is not None:
            self.response = self.data = response

        return self.response

    def http_code(self, http_code=None):
        """
        :param http_code: Set or retrieve property http_code
        :return: (int) Current/new setting
        """
        if http_code is not None:
            self.http_code = int(http_code)

        return self.http_code

    def err(self, err=None):
        """
        :param err: Set or retrieve property err
        :return: (int) Current/new setting
        """
        if err is not None:
            self.err = float(err)

        return self.err


class JamfClassic:
    """
    JamfClassic interacts with the classic API of Jamf
    """

    def __init__(self, api_url, username, password, *args, **kwargs):
        """
        Initialisation method
        :param api_url: (str) url of the api
        :param username: (str) username
        :param password: (str) password
        :param args: (list)
        :param kwargs: (dict)
        """
        self._api_url = api_url
        self._username = username
        self._password = password

        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/xml',
            'User-Agent': 'lynx',
        }
        self._timeout = int(kwargs['timoout']) if 'timeout' in kwargs else 240.0
        self._verify = bool(kwargs['verify']) if 'verify' in kwargs else True
        self._disable_warnings = bool(kwargs['disable_warnings']) if 'disable_warnings' in kwargs else False

        if self._disable_warnings:
            urllib3.disable_warnings()


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Destruction method
        :param exc_type: None
        :param exc_val: None
        :param exc_tb: None
        :return: (void)
        """
        del self._username
        del self._password

    def timeout(self, timeout=None):
        """
        Set or retrieve the timeout
        :param timeout: (int) new value or (None) to remain
        :return: (int) Current/new setting
        """
        if timeout is not None:
            self._timeout = float(timeout)

        return self._timeout

    def verify_ssl(self, verify=None):
        """
        Set or retrieve whether to verify teh SSL certificate
        :param verify: (bool) new value or (None) to remain
        :return: (bool) Current/new setting
        """
        if verify is not None and isinstance(verify, bool):
            self._verify = verify

    def disable_warnings(self):
        """
        Disable warnings for ssl verify
        Making unverified HTTPS requests is strongly discouraged, however,
        if you understand the risks and wish to disable these warnings, you can use disable_warnings()
        :param disable: (bool) new value or (None) to remain
        :return: (bool) Current/new setting
        """
        urllib3.disable_warnings()

    def get_data(self, *objects, **kwargs):
        """
        GET from the api
        :param objects: (list) of objects ex. /JSSResource/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: None
        :return:
        """
        if not objects:
            return APIResponse(response='No object specified')

        # Get data
        request_url = '{0}/JSSResource/{1}'.format(self._api_url, '/'.join(str(arg) for arg in objects))
        try:
            request = requests.get(request_url, auth=(self._username, self._password),
                                   headers=self._headers, timeout=self._timeout, verify=self._verify)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.ok:
            return APIResponse(True, request_url, request.json(), request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)

    def del_data(self, *objects, **kwargs):
        """
        DELETE to the api
        :param objects: (list) of objects ex. /JSSResource/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: None
        :return:
        """
        if not objects:
            return APIResponse(response='No object specified')

        # Dlete data
        request_url = '{0}/JSSResource/{1}'.format(self._api_url, '/'.join(str(arg) for arg in objects))
        try:
            request = requests.delete(request_url, auth=(self._username, self._password),
                                      headers=self._headers, timeout=self._timeout, verify=self._verify)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.no_content:
            return APIResponse(True, request_url, None, request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)

    def put_data(self, data, *objects, **kwargs):
        """
        PUT to the api
        :param data: (dict) data to post
        :param objects: (list) of objects ex. /JSSResource/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: None
        :return:
        """
        if not objects:
            return APIResponse(response='No object specified')

        # Put data
        request_url = '{0}/JSSResource/{1}'.format(self._api_url, '/'.join(str(arg) for arg in objects))
        try:
            request = requests.put(request_url, auth=(self._username, self._password),
                                   headers=self._headers, timeout=self._timeout, verify=self._verify, data=data)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.created:
            return APIResponse(True, request_url, None, request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)

    def post_data(self, data, *objects, **kwargs):
        """
        POST to the api
        :param data: (dict) data to post
        :param objects: (list) of objects ex. /JSSResource/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: None
        :return:
        """
        if not objects:
            return APIResponse(response='No object specified')

        # Post data
        request_url = '{0}/JSSResource/{1}'.format(self._api_url, '/'.join(str(arg) for arg in objects))
        try:
            request = requests.post(request_url, auth=(self._username, self._password),
                                    headers=self._headers, timeout=self._timeout, verify=self._verify, data=data)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.created:
            return APIResponse(True, request_url, None, request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)


class JamfUAPI:
    """
    JAMFUAP interacts with the universal API of Jamf
    """

    def __init__(self, api_url, username, password, *args, **kwargs):
        """
        Initialisation method
        :param api_url: (str) url of the api
        :param username: (str) username
        :param password: (str) password
        :param args: (list)
        :param kwargs: (dict)
        """
        self._api_url = api_url
        self._username = username
        self._password = password
        self._token = None

        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'lynx',
        }
        self._timeout = int(kwargs['timoout']) if 'timeout' in kwargs else 240.0
        self._verify = bool(kwargs['verify']) if 'verify' in kwargs else True
        self._disable_warnings = bool(kwargs['disable_warnings']) if 'disable_warnings' in kwargs else False

        if self._disable_warnings:
            urllib3.disable_warnings()

        self._login()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Destruction method
        :param exc_type: None
        :param exc_val: None
        :param exc_tb: None
        :return: (void)
        """
        try:
            requests.post(self._api_url + '/uapi/auth/invalidateToken',
                          headers=self._headers, timeout=self._timeout, verify=self._verify, data=None)
        except requests.exceptions.HTTPError:
            return None

        self._token = None
        del (self._headers['Authorization'])

    def _login(self):
        """
        Iniliaise the login
        :return: (APIResponse)
        """
        request_url = self._api_url + '/uapi/auth/tokens'

        try:
            request = requests.post(request_url, auth=(self._username, self._password),
                                    headers=self._headers, timeout=self._timeout, verify=self._verify, data=None)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.ok:
            self._token = request.json()['token']
            self._headers['Authorization'] = 'Bearer ' + self._token
            return APIResponse(True, request_url, request.text, request.status_code)
        else:
            self._token = None
            return APIResponse(False, request_url, request.text, request.status_code)

    def renew_token(self):
        """
        Renew the login token
        :return: (APIResponse)
        """
        request_url = self._api_url + '/uapi/auth/keepAlive'

        try:
            request = requests.post(request_url,
                                    headers=self._headers, timeout=self._timeout, verify=self._verify, data=None)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.ok:
            self._token = request.json()['token']
            self._headers['Authorization'] = 'Bearer ' + self._token
            return APIResponse(True, request_url, request.text, request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)

    def timeout(self, timeout=None):
        """
        Set or retrieve the timeout
        :param timeout: (int) new value or (None) to remain
        :return: (int) Current/new setting
        """
        if timeout is not None:
            self._timeout = float(timeout)

        return self._timeout

    def verify_ssl(self, verify=None):
        """
        Set or retrieve whether to verify teh SSL certificate
        :param verify: (bool) new value or (None) to remain
        :return: (bool) Current/new setting
        """
        if verify is not None and isinstance(verify, bool):
            self._verify = verify

        return self._verify

    def disable_warnings(self):
        """
        Disable warnings for ssl verify
        Making unverified HTTPS requests is strongly discouraged, however,
        if you understand the risks and wish to disable these warnings, you can use disable_warnings()
        :param disable: (bool) new value or (None) to remain
        :return: (bool) Current/new setting
        """
        urllib3.disable_warnings()

    def get_login(self):
        """
        Get login information
        :return: (APIResponse)
        """
        return self.get_data('auth')

    def get_data(self, *objects, **kwargs):
        """
        GET from the api
        :param objects: (list) of objects ex. /uapi/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: (dict) options ex: sort=asc
        :return: (APIResponse)
        """
        if not objects:
            return APIResponse(response='No object specified')

        options = []
        for kwarg in kwargs:
            options.append('{0}={1}'.format(kwarg, str(kwargs[kwarg])))

        invalid_chars = '-_.() '
        options = '?' + '&'.join(options)
        options = ''.join(char for char in options if char not in invalid_chars)

        # Get data
        request_url = '{0}/uapi/{1}{2}'.format(self._api_url, '/'.join(str(arg) for arg in objects), options)
        try:
            request = requests.get(request_url,
                                   headers=self._headers, timeout=self._timeout, verify=self._verify)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.ok:
            return APIResponse(True, request_url, request.json(), request.status_code)
        else:
            return APIResponse(False, request_url, request.text, request.status_code)

    def del_data(self, *objects, **kwargs):
        """
        DELETE from the api
        :param objects: (list) of objects ex. /uapi/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: (dict) options ex: sort=asc
        :return: (APIResponse)
        """
        if not objects:
            return APIResponse(response='No object specified')

        options = []
        for kwarg in kwargs:
            options.append('{0}={1}'.format(kwarg, str(kwargs[kwarg])))

        invalid_chars = '-_.() '
        options = '?' + '&'.join(options)
        options = ''.join(char for char in options if char not in invalid_chars)

        # Delete data
        request_url = '{0}/uapi/{1}{2}'.format(self._api_url, '/'.join(str(arg) for arg in objects), options)
        try:
            request = requests.delete(request_url,
                                      headers=self._headers, timeout=self._timeout, verify=self._verify)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.no_content:
            return APIResponse(True, url=request_url, http_code=request.status_code)
        else:
            return APIResponse(False, url=request_url, http_code=request.status_code)

    def put_data(self, data, *objects, **kwargs):
        """
        PUT to the api
        :param data: (dict) data to post
        :param objects: (list) of objects ex. /uapi/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: (dict) options ex: sort=asc
        :return: (APIResponse)
        """
        if not objects:
            return APIResponse(response='No object specified')

        options = []
        for kwarg in kwargs:
            options.append('{0}={1}'.format(kwarg, str(kwargs[kwarg])))

        invalid_chars = '-_.() '
        options = '?' + '&'.join(options)
        options = ''.join(char for char in options if char not in invalid_chars)

        # Put data
        request_url = '{0}/uapi/{1}{2}'.format(self._api_url, '/'.join(str(arg) for arg in objects), options)
        try:
            request = requests.put(request_url,
                                   headers=self._headers, timeout=self._timeout, verify=self._verify, data=data)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.created:
            return APIResponse(True, url=request_url, http_code=request.status_code)
        else:
            return APIResponse(False, url=request_url, http_code=request.status_code)

    def post_data(self, data, *objects, **kwargs):
        """
        POST to the api
        :param data: (dict) data to post
        :param objects: (list) of objects ex. /uapi/computer/id/0 = [ 'computer', 'id', 0]
        :param kwargs: (dict) options ex: sort=asc
        :return: (APIResponse)
        """
        if not objects:
            return APIResponse(response='No object specified')

        options = []
        for kwarg in kwargs:
            options.append('{0}={1}'.format(kwarg, str(kwargs[kwarg])))

        invalid_chars = '-_.() '
        options = '?' + '&'.join(options)
        options = ''.join(char for char in options if char not in invalid_chars)

        # Post data
        request_url = '{0}/uapi/{1}{2}'.format(self._api_url, '/'.join(str(arg) for arg in objects), options)
        try:
            request = requests.post(request_url,
                                    headers=self._headers, timeout=self._timeout, verify=self._verify, data=data)
        except requests.exceptions.HTTPError as err:
            return APIResponse(url=request_url, err=err)

        if request.status_code == requests.codes.created:
            return APIResponse(True, url=request_url, http_code=request.status_code)
        else:
            return APIResponse(False, url=request_url, http_code=request.status_code)

