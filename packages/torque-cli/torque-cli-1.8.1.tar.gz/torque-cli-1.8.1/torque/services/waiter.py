import datetime
import time

from yaspin import yaspin

from torque.branch.branch_context import ContextBranch
from torque.branch.branch_utils import logger  # can_temp_branch_be_deleted, logger
from torque.commands.base import BaseCommand
from torque.constants import DEFAULT_TIMEOUT, FINAL_SB_STATUSES
from torque.environments import EnvironmentsManager


class Waiter(object):
    @staticmethod
    def wait_for_environment_to_launch(
        command: BaseCommand,
        env_manager: EnvironmentsManager,
        env_id: str,
        timeout: int,
        context_branch: ContextBranch,
        wait: bool,
    ) -> bool:

        if not wait and not context_branch.temp_branch_exists:
            return False
        try:
            if context_branch.temp_branch_exists:
                context_branch.revert_from_local_temp_branch()

            if not timeout:
                timeout = DEFAULT_TIMEOUT

            start_time = datetime.datetime.now()
            environment = env_manager.get(env_id)
            status = getattr(environment, "environment_status")

            environment_start_wait_output(command, env_id, context_branch.temp_branch_exists)

            spinner_class = NullSpinner if command.global_input_parser.output_json else yaspin

            with spinner_class(text="Starting...", color="yellow") as spinner:
                while (datetime.datetime.now() - start_time).seconds < timeout * 60:
                    if status in FINAL_SB_STATUSES:
                        spinner.green.ok("✔")
                        break
                    # TODO(ddovbii): Disable temporary branch for now

                    #  if context_branch.temp_branch_exists and can_temp_branch_be_deleted(environment):
                    #     context_branch.delete_temp_branch()
                    #     if not wait:
                    #         spinner.green.ok("✔")
                    #         break

                    time.sleep(5)
                    spinner.text = f"[{int((datetime.datetime.now() - start_time).total_seconds())} sec]"
                    environment = env_manager.get(env_id)
                    status = getattr(environment, "environment_status")
                else:
                    logger.error(f"Timeout Reached - Environment {env_id} was not active after {timeout} minutes")
                    return True
            return False

        except Exception as e:
            logger.error(f"There was an issue with waiting for environment deployment -> {str(e)}")


def environment_start_wait_output(command: BaseCommand, environment_id, temp_branch_exists):
    if temp_branch_exists:
        logger.debug(f"Waiting before deleting temp branch that was created for this environment (id={environment_id})")
        command.fyi_info("Canceling or exiting before the process completes may cause the environment to fail")
        command.info("Waiting for the Environment to start with local changes. This may take some time.")
    else:
        logger.debug(f"Waiting for the Environment {environment_id} to finish launching...")
        command.info("Waiting for the Environment to start. This may take some time.")


class NullSpinner:
    text: str

    def __init__(self, text, color):
        self.green = NullSpinnerOut()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class NullSpinnerOut:
    def ok(self, text) -> None:
        pass
