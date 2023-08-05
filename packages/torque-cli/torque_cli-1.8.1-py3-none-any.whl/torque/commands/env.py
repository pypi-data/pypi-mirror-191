from torque.branch.branch_context import ContextBranch
from torque.branch.branch_utils import get_and_check_folder_based_repo, logger
from torque.commands.base import BaseCommand
from torque.environments import EnvironmentsManager
from torque.models.blueprints import BlueprintsManager
from torque.parsers.command_input_validators import CommandInputValidator
from torque.services.sb_naming import generate_environment_name
from torque.services.waiter import Waiter


class EnvironmentsCommand(BaseCommand):
    """
    usage:
        torque (env | environment) start <blueprint_name> [options] [--output=json]
        torque (env | environment) status <environment_id> [--output=json]
        torque (env | environment) get <environment_id> [--output=json | --output=json --detail]
        torque (env | environment) end <environment_id>
        torque (env | environment) list [--filter={all|my|auto}] [--show-ended] [--count=<N>] [--output=json]
        torque (env | environment) [--help]

    options:
       -h --help                        Show this message

       -d, --duration <minutes>         The Environment will automatically de-provision at the end of the provided
                                        duration.

       -n, --name <environment_name>    Provide a name for the Environment. If not set, the name will be generated
                                        automatically using the source branch (or local changes) and current time.

       -i, --inputs <input_params>      The Blueprints inputs can be provided as a comma-separated list of key=value
                                        pairs. For example: key1=value1, key2=value2.
                                        By default Torque CLI will try to take the default values for these inputs
                                        from the Blueprint definition yaml file.

       -r, --repo <repository_name>     Set the name of the repository where the source blueprint is published

       -b, --branch <branch>            Run the Blueprint version from a remote Git branch. If not provided,
                                        the CLI will attempt to automatically detect the current working branch.
                                        The CLI will automatically run any local uncommitted or untracked changes in a
                                        temporary branch created for the validation or for the development Environment.

       -c, --commit <commitId>          Specify a specific Commit ID. This is used in order to run a environment from a
                                        specific Blueprint historic version. If this parameter is used, the
                                        Branch parameter must also be specified.

       -t, --timeout <minutes>          Set how long (default timeout is 30 minutes) to block and wait before releasing
                                        control back to shell prompt. If timeout is reached before the desired status
                                        the wait loop will be interrupted.
                                        If "wait_active" flag is not set and a temp branch is created for local changes,
                                        the CLI will block and wait until the Environment Infrastructure and Artifacts
                                        are ready. Then the temp branch can be safely deleted and the wait loop will
                                        end. If "wait_active" flag is set, the CLI will block and wait until the
                                        environment is Active regardless if temp branch is created or not.

       -w, --wait_active                Block shell prompt and wait for the Environment to be Active (or deployment
                                        ended with an error) while the timeout is not reached.
                                        Default timeout is 30 minutes.
                                        The default timeout can be changed using the "timeout" flag.

       -o --output=json                 Yield output in JSON format
    """

    RESOURCE_MANAGER = EnvironmentsManager

    def get_actions_table(self) -> dict:
        return {
            "status": self.do_status,
            "start": self.do_start,
            "end": self.do_end,
            "list": self.do_list,
            "get": self.do_get,
        }

    def do_list(self):
        list_filter = self.input_parser.environment_list.filter
        show_ended = self.input_parser.environment_list.show_ended
        count = self.input_parser.environment_list.count

        try:
            env_list = self.manager.list(filter_opt=list_filter, count=count)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        if not show_ended:
            env_list = list(filter(lambda sb: sb.environment_status != "Ended", env_list))

        return True, env_list

    def do_status(self):
        try:
            env = self.manager.get(self.input_parser.environment_status.environment_id)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        status = getattr(env, "environment_status")
        return True, status

    def do_get(self):
        try:
            detail = self.input_parser.blueprint_list.detail
            if detail:
                env = self.manager.get_detailed(self.input_parser.environment_status.environment_id)
            else:
                env = self.manager.get(self.input_parser.environment_status.environment_id)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        return True, env

    def do_end(self):
        try:
            self.manager.end(self.input_parser.environment_status.environment_id)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        return self.success("End request has been sent")

    def do_start(self):
        # get commands inputs
        blueprint_name = self.input_parser.environment_start.blueprint_name

        branch = self.input_parser.environment_start.branch
        commit = self.input_parser.environment_start.commit

        CommandInputValidator.validate_commit_and_branch_specified(branch, commit)

        env_name = self.input_parser.environment_start.environment_name
        timeout = self.input_parser.environment_start.timeout
        wait = self.input_parser.environment_start.wait
        duration = self.input_parser.environment_start.duration
        inputs = self.input_parser.environment_start.inputs
        repo_name = self.input_parser.environment_start.repo_name

        if not branch:
            try:
                repo = get_and_check_folder_based_repo(blueprint_name)
            except Exception:
                # self.info(
                #     "Since the blueprint repo was not found in the local working directory, trying to find blueprint "
                #     "remotely and start it from the default branch."
                # )
                repo = None
            try:
                self._update_missing_inputs_with_default_values(blueprint_name, inputs, repo, repo_name)
            except Exception as e:
                logger.exception(e, exc_info=False)
                return self.die(f"Unable to start environment from blueprint '{blueprint_name}'")
        else:
            repo = None

        with ContextBranch(repo, branch) as context_branch:
            # TODO move error handling to exception catch (investigate best practices of error handling)

            if env_name is None:
                env_name = generate_environment_name(
                    blueprint_name,
                    context_branch.temp_working_branch,
                    context_branch.working_branch,
                )

            try:
                environment_id = self.manager.start(
                    env_name,
                    blueprint_name,
                    repo_name,
                    duration,
                    context_branch.validation_branch,
                    commit,
                    inputs,
                )
                if not self.global_input_parser.output_json:
                    self.action_announcement("Starting environment")
                    self.important_value("Id: ", environment_id)
                    self.url(prefix_message="URL: ", message=self.manager.get_environment_ui_link(environment_id))

            except Exception as e:
                logger.exception(e, exc_info=False)
                return self.die()

            wait_timeout_reached = Waiter.wait_for_environment_to_launch(
                self,
                self.manager,
                environment_id,
                timeout,
                context_branch,
                wait,
            )

            if wait_timeout_reached:
                return self.die()
            elif self.global_input_parser.output_json:
                return True, environment_id
            else:
                return self.success(environment_id)

    def _update_missing_inputs_with_default_values(self, blueprint_name, inputs, repo, repo_name):
        # TODO(ddovbii): This obtaining default values magic must be refactored
        if repo is not None:
            logger.debug("Trying to obtain default values for inputs from local git blueprint repo")
            try:
                if not repo.is_current_branch_synced():
                    logger.debug("Skipping obtaining values since local branch is not synced with remote")
                else:
                    for input_name, input_value in repo.get_blueprint_default_inputs(blueprint_name).items():
                        if input_name not in inputs and input_value is not None:
                            logger.debug(f"Parameter `{input_name}` has been set with default value `{input_value}`")
                            inputs[input_name] = input_value

            except Exception as e:
                logger.debug(f"Unable to obtain default values. Details: {e}")
        else:
            bp_manager = BlueprintsManager(client=self.client)
            try:
                blueprint_object = bp_manager.get_detailed(blueprint_name, repo_name)
            except Exception as e:
                raise Exception(f"Unable to get details of blueprint '{blueprint_name}'. Details: {e}")
            bp_props = blueprint_object.get("details", None) or blueprint_object

            for inp in bp_props.get("inputs", []):
                name = inp["name"]
                default = inp.get("default_value", None)
                if name not in inputs and default is not None:
                    logger.debug(f"Parameter `{name}` has been set with default value `{default}")
                    inputs[name] = default

        return repo
