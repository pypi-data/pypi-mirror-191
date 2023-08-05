import base64
import logging
from typing import Any

from torque.commands.base import BaseCommand
from torque.models.blueprints import BlueprintsManager

logger = logging.getLogger(__name__)


class BlueprintsCommand(BaseCommand):
    """
    usage:
        torque (bp | blueprint) list [--output=json | --output=json --detail]
        torque (bp | blueprint) validate <file> [--output=json | --output=json --detail]
        torque (bp | blueprint) get <name> [--repo=<repo_name>] [--output=json | --output=json --detail]
        torque (bp | blueprint) [--help]

    options:
       -o --output=json           Yield output in JSON format

       -s --source=<source_type>  Specify a type of blueprint source: 'torque' or 'git'. [default: git]

       -d --detail                Obtain full blueprint data in JSON format

       -h --help                  Show this message

    When validating a blueprint, you can use "-" to read data from stdin instead of <file>
    """

    RESOURCE_MANAGER = BlueprintsManager

    def get_actions_table(self) -> dict:
        return {
            "list": self.do_list,
            "validate": self.do_validate,
            "get": self.do_get,
        }

    def do_list(self) -> (bool, Any):
        detail = self.input_parser.blueprint_list.detail
        try:
            if detail:
                blueprint_list = self.manager.list_detailed()
            else:
                blueprint_list = self.manager.list()
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        return True, blueprint_list

    def do_get(self) -> (bool, Any):
        detail = self.input_parser.blueprint_get.detail
        blueprint_name = self.input_parser.blueprint_get.blueprint_name
        repo = self.input_parser.blueprint_get.repo

        try:
            if detail:
                bp = self.manager.get_detailed(blueprint_name, repo_name=repo)
            else:
                bp = self.manager.get(blueprint_name, repo)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die(f"Unable to get details of blueprint '{blueprint_name}'")

        return True, bp

    def do_validate(self) -> (bool, Any):
        blueprint = self.input_parser.blueprint_validate.blueprint
        encoded = base64.b64encode(blueprint.encode("utf-8"))

        try:
            bp = self.manager.validate(b64_blueprint_content=encoded.decode("utf-8"))
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        errors = bp.get("errors", [])

        if errors:
            logger.info("Blueprint validation failed")
            return False, errors

        else:
            return self.success("Blueprint is valid")
