from urllib.parse import urljoin

from torque.client import TorqueClient

# TODO(ddovbii): Make classes abstract

# todo - alexa - its like a wrapper around our api


class ResourceManager(object):
    resource_obj = None

    def __init__(self, client: TorqueClient):
        self.client = client
        self.endpoint = urljoin(self.client.base_url, f"spaces/{self.client.space}/")

    def _get_full_url(self, path: str):
        url = urljoin(self.endpoint, path)
        return url

    def _get(self, path: str, headers: dict = None, query_params: dict = None):
        if headers is None:
            headers = {}

        url = urljoin(self.endpoint, path)

        result = self.client.request(url, "GET", headers, query_params=query_params)
        return result.json()

    def _delete(self, path: str, query_params: dict = None):
        url = urljoin(self.endpoint, path)

        result = self.client.request(url, "DELETE", query_params=query_params)
        return result

    def _list(self, path: str, filter_params: dict = None, query_params: dict = None):
        url = urljoin(self.endpoint, path)

        # TODO(ddovbii): add filter handling
        # if filter is not None:
        params = filter_params.copy() if filter_params else None

        result = self.client.request(url, "GET", params=params)

        return result.json()

    def _post(self, path: str, params: dict = None, headers: dict = None, query_params: dict = None):
        if headers is None:
            headers = {}

        if params is None:
            params = {}

        url = urljoin(self.endpoint, path)
        result = self.client.request(url, "POST", params, headers)
        return result.json()


class Resource(object):
    def __init__(self, manager: ResourceManager):
        self.manager = manager

    @classmethod
    def json_deserialize(cls, manager: ResourceManager, json_obj: dict):
        pass

    def json_serialize(self) -> dict:
        pass

    def table_serialize(self) -> dict:
        pass
