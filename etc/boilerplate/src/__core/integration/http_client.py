import json
from urllib.request import HTTPError, Request, urlopen

Body = dict[str, any]
Headers = dict[str, any]
Response = tuple[int, str | None]

DEFAULT_TIMEOUT = 120

class HttpClient:
  def __init__(self, host: str, timeout: int = DEFAULT_TIMEOUT):
    self.__host = host
    self.__timeout = timeout

  def post(self, path: str, body: Body = None, headers: Headers = {}) -> Response:
    return self.__request("POST", path, body, headers)

  def put(self, path: str, body: Body = None, headers: Headers = {}) -> Response:
    return self.__request("PUT", path, body, headers)

  def delete(self, path: str, body: Body = None, headers: Headers = {}) -> Response:
    return self.__request("DELETE", path, body, headers)

  def get(self, path: str, headers: Headers = {}) -> Response:
    return self.__request("GET", path, None, headers)

  def __request(
    self,
    method: str,
    path: str,
    body: Body,
    headers: Headers
  ) -> Response:
    request = Request(
      url=f"{self.__host}/{path}",
      data=json.dumps(body).encode() if body else None,
      headers=headers,
      method=method,
    )

    status_code = 0
    response_text = None
    try:
      with urlopen(request, timeout=self.__timeout) as response:
        status_code = response.status
        response_text = response.read()
    except HTTPError as ex:
      status_code = ex.status
      response_text = ex.read()

    return [status_code, response_text]
