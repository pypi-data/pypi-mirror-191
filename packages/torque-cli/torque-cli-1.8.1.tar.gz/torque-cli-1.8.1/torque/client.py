import logging
import os
import urllib.parse as urlparse

import pkg_resources
from requests import Response, Session

from .exceptions import Unauthorized
from .session import TorqueSession

logging.getLogger("urllib3").setLevel(logging.WARNING)


class TorqueClient(object):
    """Base class for Torque API access"""

    API_URL = "api/"

    def __init__(
        self,
        torque_host_prefix: str = "https://",
        torque_host: str = "portal.qtorque.io",
        space: str = None,
        token: str = None,
        account: str = None,
        email: str = None,
        password: str = None,
        session: TorqueSession = TorqueSession(),
    ):

        if os.environ.get("TORQUE_HOSTNAME"):
            torque_host = os.environ["TORQUE_HOSTNAME"]

        self.base_url = urlparse.urljoin(f"{torque_host_prefix}{torque_host}", self.API_URL)

        self.session = session
        self.space = space
        self.account = account

        if token:
            self.token = token

        elif all([account, email, password]):
            self.token = TorqueClient.login(account, email, password, self.session, self.base_url)

        self.session.init_bearer_auth(token)

    def __del__(self):
        if self.session:
            try:
                self.session.close()
            except Exception:
                raise
            finally:
                self.session = None

    def login(
        self,
        account: str,
        email: str,
        password: str,
        session: Session = TorqueSession(),
    ):
        path = urlparse.urljoin(self.base_url, f"accounts/{account}/login")
        payload = {"email": email, "password": password}
        resp = session.post(url=path, json=payload)
        if resp.status_code != 200:
            # TODO(ddovbii): implement exceptions and error handler
            raise Unauthorized("Login Failed")

        return resp.json().get("access_token", "")

    def longtoken(self):
        url_longtoken = urlparse.urljoin(self.base_url, "token/longtoken")
        longtoken_resp = self.session.post(url_longtoken)
        return longtoken_resp.json().get("access_token", "")

    def request(
        self, endpoint: str, method: str = "GET", params: dict = None, headers: dict = None, query_params: dict = None
    ) -> Response:
        """Gets response as Json"""
        method = method.upper()

        if method not in ("GET", "PUT", "POST", "DELETE"):
            raise ValueError("Method must be in [GET, POST, PUT, DELETE]")

        if headers:
            self.session.headers.update(headers)

        version = pkg_resources.get_distribution("torque-cli").version
        ua_header = os.environ.get("TORQUE_USERAGENT", None)

        if ua_header:
            self.session.headers.update({"User-Agent": ua_header})

        elif version:
            self.session.headers.update({"User-Agent": f"Torque-CLI/{version}"})

        if method in ("POST", "PUT", "DELETE"):
            self.session.headers.update({"Content-Type": "application/json"})

        if params is None:
            params = {}

        url = urlparse.urljoin(self.base_url, endpoint)

        if query_params:
            url_parts = list(urlparse.urlparse(url))
            url_parts[4] = urlparse.urlencode(query_params)
            url = urlparse.urlunparse(url_parts)

        request_args = {
            "method": method,
            "url": url,
        }

        if method == "GET":
            request_args["params"] = params
        else:
            request_args["json"] = params

        response = self.session.request(**request_args)

        if response.status_code >= 400:
            # TODO(ddovbii): implement exceptions and error handler
            message = ";".join([f"{err['name']}: {err['message']}" for err in response.json().get("errors", [])])
            raise Exception(message)

        return response
