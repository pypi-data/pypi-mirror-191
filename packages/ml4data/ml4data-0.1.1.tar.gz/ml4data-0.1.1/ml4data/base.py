import requests
from typing import Any, BinaryIO, Dict, List, Optional

class APIException(Exception):
    def __init__(self, msg: str, status_code: int):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return "[{status_code}] Error: {msg}".format(status_code=self.status_code,
                                                     msg=self.msg)

class AuthenticationError(APIException):
    def __init__(self, msg: str):
        super(AuthenticationError, self).__init__(msg, 401)


class ML4DataClient(object):
    """ Base class for all ML4Data clients
    """
    base_url = 'https://api.ml4data.com/api'
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers = {"API-Key": self.token,
                                "User-Agent": 'ml4data-client'}

    def _make_request(self,
                      method: str,
                      endpoint: str,
                      params: Optional[Dict[str, str]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      files: Optional[Dict[str, BinaryIO]] = None) -> Any:
        url = self.base_url + endpoint
        resp = self.session.request(url=url,
                                    method=method,
                                    params=params,
                                    data=data,
                                    files=files)
        if resp.status_code != 200:
            if resp.status_code == 401:
                raise AuthenticationError(resp.json()['error']['message'])
            else:
                raise APIException(resp.json()['error']['message'], status_code=resp.status_code)
        return resp.json()['result']

    def _get(self,
             endpoint: str,
             params: Optional[Dict[str, str]] = None) -> Any:
        return self._make_request(method='GET',
                                  endpoint=endpoint,
                                  params=params)

    def _post(self,
              endpoint: str,
              params: Optional[Dict[str, str]] = None,
              data: Optional[Dict[str, Any]] = None,
              files: Optional[Dict[str, BinaryIO]] = None) -> Any:
        return self._make_request(method='POST',
                                  endpoint=endpoint,
                                  params=params,
                                  data=data,
                                  files=files)

    def __del__(self):
        self.session.close()
