from typing import List
from urllib.parse import urlparse

from .base import Resource, ResourceManager


class Environment(Resource):
    def __init__(self, manager: ResourceManager, environment_id: str, name: str, blueprint_name: str):
        super(Environment, self).__init__(manager)

        self.environment_id = environment_id
        self.name = name
        self.blueprint_name = blueprint_name

    @classmethod
    def json_deserialize(cls, manager: ResourceManager, json_obj: dict):
        try:
            environment_id = json_obj.get("id", None) or json_obj["details"]["id"]
            env_details = json_obj["details"]["definition"]
            env = Environment(
                manager,
                environment_id,
                env_details["metadata"]["name"],
                env_details["metadata"]["blueprint_name"],
            )
            env.environment_status = json_obj["details"]["computed_status"]
        except KeyError as e:
            raise NotImplementedError(f"unable to create object. Missing keys in Json. Details: {e}")

        # for attr in ["description", "errors", "sandbox_status", "launching_progress"]:
        #     sb.__dict__[attr] = json_obj.get(attr, "")
        # TODO(ddovbii): set all needed attributes
        # sb.errors = json_obj.get("errors", [])
        # sb.description = json_obj.get("description", "")
        # sb.status = json_obj.get("sandbox_status", "")
        # sb.launching_progress = json_obj.get("launching_progress", {})
        # sb.__dict__ = json_obj.copy()
        return env

    def json_serialize(self) -> dict:
        return {
            "id": self.environment_id,
            "name": self.name,
            "blueprint_name": self.blueprint_name,
        }

    def table_serialize(self) -> dict:
        return self.json_serialize()


class EnvironmentsManager(ResourceManager):
    resource_obj = Environment
    ENVIRONMENTS_PATH = "environments"
    ENVIRONMENTS_LINK = "sandboxes"

    # SPECIFIC_SANDBOX_PATH = "sandboxes"

    def get_environment_url(self, env_id: str) -> str:
        return self._get_full_url(f"{self.ENVIRONMENTS_PATH}/{env_id}")

    def get_environment_ui_link(self, env_id: str) -> str:
        url = urlparse(self.get_environment_url(env_id))
        space = url.path.split("/")[3]
        return f"https://{url.hostname}/{space}/{self.ENVIRONMENTS_LINK}/{env_id}"

    def get(self, environment_id: str) -> Environment:
        url = f"{self.ENVIRONMENTS_PATH}/{environment_id}"
        env_json = self._get(url)

        return self.resource_obj.json_deserialize(self, env_json)

    def get_detailed(self, environment_id: str) -> dict:
        url = f"{self.ENVIRONMENTS_PATH}/{environment_id}"
        sb_json = self._get(url)

        return sb_json

    def list(self, count: int = 25, filter_opt: str = "my") -> List[Environment]:

        filter_params = {"count": count, "filter": filter_opt}
        list_json = self._list(path=self.ENVIRONMENTS_PATH, filter_params=filter_params)

        return [self.resource_obj.json_deserialize(self, obj) for obj in list_json]

    def start(
        self,
        environment_name: str,
        blueprint_name: str,
        repo_name: str,
        duration: int = 120,
        branch: str = None,
        commit: str = None,
        inputs: dict = None,
    ) -> str:

        if commit and not branch:
            raise ValueError("Commit is passed without branch")

        iso_duration = f"PT{duration}M"

        params = {
            "environment_name": environment_name,
            "duration": iso_duration,
            "inputs": inputs,
            "source": {
                # "blueprint_source_type": source_type_map.get(source, None),
                "blueprint_name": blueprint_name,
                "repository_name": repo_name,
            },
        }

        if branch:
            params["source"]["branch"] = branch
            params["source"]["commit"] = commit or ""

        result_json = self._post(self.ENVIRONMENTS_PATH, params)
        env_id = result_json["id"]
        return env_id

    def end(self, env_id: str):
        url = f"{self.ENVIRONMENTS_PATH}/{env_id}"

        try:
            self.get(env_id)

        except Exception as e:
            raise NotImplementedError(f"Unable to end environment with ID: {env_id}. Details: {e}")

        self._delete(url)
