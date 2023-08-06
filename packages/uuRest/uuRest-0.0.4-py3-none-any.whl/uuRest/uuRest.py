from typing import List, Dict, Type, TypeVar
from lib.ts.core.common import GraphObject, tab, instantiate
import requests
import json
from requests.auth import HTTPBasicAuth
from enum import Enum
from lib.common.logging import log, log_warning, log_error, log_fatal
from lib.common.utils import Stopwatch
import lib.common.io as io
import uuRestLogin


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class uuRestMethod(Enum):
    GET = "GET"
    POST = "POST"

    def __str__(self):
        if self == uuRestMethod.GET:
            return "GET"
        elif self == uuRestMethod.POST:
            return "POST"
        else:
            return "UNKNOWN"

class TokenType(Enum):
    GENERAL = "GENERAL"
    PLUS4U = "PLUS4U"


class RestException(Exception):
    def __init__(self, command: str, query: str, call_method: uuRestMethod, request, response, http_status_code):
        """
        Vytvori tridu vyjimky pro Rest API, ktera se muze pouzit pokud dojde k selhani restoveho volani
        :param request:
        :param response:
        """
        self.command = command
        self.query = query
        self.call_method = call_method
        self.request = request
        self.response = response
        self.http_status_code = http_status_code


class RestApiCallHistory:
    def __init__(self, buffer_size: int = 100):
        """
        Vytvori objekt pro ulozeni historie volani rest api
        :param buffer_size:
        """
        self.buffer = {
            "total_calls": 0,
            "rest_api_call_history": []
        }
        self.buffer_size = buffer_size

    def add_history_item(self, command: str, query: str, call_method: uuRestMethod, request, response, http_status_code):
        """
        Prida novy zaznam o volani do bufferu
        :param command:
        :param query:
        :param method:
        :param request:
        :param response:
        :param response_http_code:
        :return:
        """
        history_item = {
            ""
            "data": command,
            "query": query,
            "method": str(call_method),
            "request": request,
            "response": response,
            "http_status_code": http_status_code
        }
        self.buffer["total_calls"] += 1
        self.buffer["rest_api_call_history"].append(history_item)
        # pokud je buffer vetsi nez buffer_size, tak odebere prvni prvek pole
        if len(self.buffer["rest_api_call_history"]) > self.buffer_size:
            self.buffer["rest_api_call_history"].pop(0)


class uuRest:
    def __init__(self, login: uuRestLogin.uuRestLogin, commands_url_prefix: str = ""):
        """
        Vytvori tridu pro rest api a ziska token
        :param api_url:
        :param oidc_url:
        :param login:
        :param password:
        """
        # nastavi zakladni promenne
        self._login: uuRestLogin.uuRestLogin = login
        self.commands_url_prefix = commands_url_prefix
        self._token = None
        self._token_renew = 0

    @property
    def login(self):
        return self._login

    @property
    def token(self) -> str:
        if type(self._login) == uuRestLogin.uuRestLoginGeneral:
            self._load_token_general()
        else:
            self.load_token_plus4u(state=self.state)

    @token.setter
    def token(self, value: str):
        self._token = value

    @token.deleter
    def token(self):
        del self._token

    def _load_token_general(self):
        # if rest api is not properly set then return
        data_str = json.dumps(self._login.get_request_payload())
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        r = requests.post(self._login.oidc_url, data=data_str, verify=False, headers=headers)
        if r.status_code == 200:
            token_response = r.json()
            self._token = token_response['id_token']
            self._token_renew = token_response["expires_in"] - 100
        # zkusi se prihlasit pomoci access kodu
        else:
            raise Exception(f'Cannot load token. Response status is {str(r.status_code)}.\n{r.text}')

    def load_token_plus4u(self, state: str):
        # if rest api is not properly set then return
        if not self.is_properly_set():
            return
        # otherwise load token
        data = {
            "grant_type": "password",
            "response_type": "id_token",
            "rememberMe": False,
            "accessCode1": f"{self.login}",
            "accessCode2": f"{self.password}",
            "state": state,
            "scope": f'openid {self.api_url}'
        }
        data_str = json.dumps(data)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        #state = f'QNSKr7tTt83rTdth.ahg8xNoQMjOAY1nxTROVxebtX8d2o-9Q4M4MmwQlXMqDSBS0L_qzrdiI3FwOEHIifQ-2SavNtu_WDZMP_c5iujuCWNr9ykeMhMw0BeHfvdF1gOyNOb96AZU7V-xRGQPgrYQMQUyYy42EcKiHeoaMMJgmw8ZwXiecdYGa0VjkxmusmqhcL3R68aYKBcDNasMVeRQILFVFpCc3CAKDo5v0Zh3nfU-fcfBnvHVodehdwTIOGlqBWYwFwQQzrtqGdkyhrtYSEq2gggj6AkljvKjkk1y9pi3oFmVA0lUkitEvIeXoCQaquFJs0T6_33IUqZBGw8OQ81K00v6bnH-G0HZp5sN3gwniohzwQHUYEJFeFMF8C-Toeo2QB-Y1pdEffOqxRdiaMk7msy2k-sPvr2ruU60FYrYIsRBVKzudfF3CDCZov3YPWI4nTv5ZDk8jo2sQGk56q6ewDtVyB-L8qhlsaK1PXZEKeTTDXpX6D7bKtHm4IS8Ulgh5NDy67MTWIYZMP5eOe25U5C7RJDy6ykLAQg9-45ICzXYd6hQDh-6OUg5m3nqRJCaRlarPXl0tfjlps3ujga8HWpQvmxCH62CHCEqRtyZukrjgsgyi0bZl3dBQaSFjw3j0NOHG1TtlJqLBNJEkICbb1OPQ9I8G_G5yV8HGEqbydzOzLw%3D%3D'
        url_parameters = f'state={state}&rememberMe=false&accessCode1={self.login}&accessCode2={self.password}'
        r = requests.post(self.oidc_url + f'?' + url_parameters, data=data_str, verify=False, headers=headers)
        if r.status_code == 200:
            token = r.history[1].raw.headers["location"]
            token = token.split("id_token=")[1]
            token = token.split("&")[0]
            self._token = token
            self._token_renew = 1500
        else:
            raise Exception(f'Cannot load token. Response status is {str(r.status_code)}.\n{r.text}')

    def call_raw(self, command: str, request: Dict or json or str, method: uuRestMethod = uuRestMethod.POST, raise_exception_on_error: bool = True) -> dict:
        return {}

    def call(self, command: str, request: Dict or json or str, method: uuRestMethod = uuRestMethod.POST, trigger_fatal_error: bool = True,
             is_paged_call: bool = False) -> json:
        """
        Zavola server
        :param is_paged_call: indikuje jestli se jedna o data typu List se strankovanim
        :param trigger_fatal_error:
        :param method:
        :param command:
        :param request:
        :param ttl:
        :return:
        """
        # pokud uz uplynul stanoveny cas, tak aktualizuje token
        if self.stopwatch.get_run_time_in_seconds() > self.renew_token:
            self.load_token()
        # upravi data a data
        command = command.lstrip('/')
        if isinstance(request, dict):
            # pokud se jedna o data typu List tak zvetsi pocet elementu, ktere se vejdou na stranku
            # TODO tento kod je nutne opravit
            if is_paged_call:
                request.update({"pageInfo": {"pageIndex": 0, "pageSize": 1000}})
            data_str = json.dumps(request)
        # elif isinstance(data, json):
        #     data_str = json.dumps(data)
        elif isinstance(request, str):
            data_str = request
        else:
            raise Exception(f'Parameter data must be either dict, json or str.')
        # aplikuje replace na command
        data_str = Rest.apply_global_replace_strings(data_str)
        # provola server
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        query = f'{self.api_url}/{command}'
        if method == uuRestMethod.POST:
            r = requests.post(query, data=data_str, verify=False, auth=BearerAuth(self.token), headers=headers)
        else:
            r = requests.get(query, data=data_str, verify=False, auth=BearerAuth(self.token), headers=headers)
        # vrati vysledek requestu
        result = r.content
        result = result.decode("utf-8")
        result = json.loads(result)
        # ulozi volani do historie
        self.history.add_history_item(command=command, query=query, call_method=method, request=request, response=result, http_status_code=r.status_code)
        # zjisti, jestli soucasti response není chyba jiná než "unsupportedKeys" z create commandu (nechceme, aby se opakovalo, v případě, že create vrátí 200 s unsupportedKeys (například id))
        if r.status_code != 200 or (result["uuAppErrorMap"] != {} and (len(list(result["uuAppErrorMap"].keys())) > 1 or not list(result["uuAppErrorMap"].keys())[0].endswith("create/unsupportedKeys"))):
            # pokusi se opravit zname chyby
            if trigger_fatal_error:
                # pokusi se vyresit problem
                original_request = json.dumps(request, indent=4)
                original_response = json.dumps(result, indent=4)
                result, problem_solved = self._solve_call_error(command=command, request=request, method=method, trigger_fatal_error=trigger_fatal_error,
                                                                is_paged_call=is_paged_call, last_response=result)
                # pokud se problem nepodarilo vyresit tak zobrazi chybu
                if not problem_solved:
                    log_error(f'Error during rest_api call "{query}".')
                    log_error(f'Status code is {str(r.status_code)}.')
                    log_error(f'Original request was:')
                    #log_error(f'{data_str}')
                    log_error(f'{original_request}')
                    log_error(f'Original response was:')
                    log_error(f'{original_response}')
                    log_error(f'Last request after several attempts to solve the problem was:')
                    log_error(f'{json.dumps(request, indent=4)}')
                    log_error(f'Last response after several attempts to solve the problem was:')
                    log_error(f'{json.dumps(result, indent=4)}')
                    raise RestException(command=command, query=query, call_method=method, request=request, response=result, http_status_code=r.status_code)
        return result

