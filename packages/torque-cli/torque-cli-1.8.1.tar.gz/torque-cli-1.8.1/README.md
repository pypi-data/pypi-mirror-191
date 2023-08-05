# Quali Torque CLI

[![Coverage Status](https://coveralls.io/repos/github/QualiTorque/torque-cli/badge.svg?branch=master)](https://coveralls.io/github/QualiTorque/torque-cli?branch=master)
[![CI](https://github.com/QualiTorque/torque-cli/workflows/CI/badge.svg)](https://github.com/QualiTorque/torque-cli/actions?query=workflow%3ACI)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/torque-cli.svg)](https://badge.fury.io/py/torque-cli)
[![Maintainability](https://api.codeclimate.com/v1/badges/763f7e7153d86bd91e02/maintainability)](https://codeclimate.com/github/QualiTorque/torque-cli/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

![quali](quali.png)

## Intro

Torque CLI is the command-line tool for interacting with [Torque](https://qtorque.io), the EaaS platform.
To learn more about Torque, visit [https://qtorque.io](https://qtorque.io).

## Why use Torque CLI

When developing Blueprints for Torque, it can be very helpful to immediately check your work for errors.

Let's assume you are currently working in *development* branch, and you also have a main branch which is connected
to a Torque space. You would like to be sure that your latest local changes haven't broken anything before committing to current branch and pushing to remote or before merging changes to main branch.

This is where this tool might be handy for you. Instead of reconnecting Torque to your development branch in the UI or going with "merge and pray" you can
use Torque CLI to validate your current Blueprints state and even launch Environments.

> **_NOTE:_**  Please note that the latest stable version with spec1 support is **1.5.2**.
Some features described in this manual (like blueprint validation or temporary branch workflow)
are not implemented yet in the **>1.6.x** version with spec2 support, but they are coming soon.

## Installing

You can install Torque CLI with [pip](https://pip.pypa.io/en/stable/):

`$ python -m pip install torque-cli`

Or if you want to install it for your user:

`$ python -m pip install --user torque-cli`

### Configuration

In order to allow the CLI tool to authenticate with Torque you must provide several parameters:
* *Token* The easiest way to generate a token is via the Torque UI. Navigate to *Settings (in your space) -> Integrations ->
click “Connect” under any of the CI tools -> click “New Token”* to get an API token. Alternatively, a token can be generated using
```torque configure set --login``` command
* *Space* The space in the Torque to use which is mapped to the Git repo you are using
* *Account* (optional) providing the account name

The *Token*, *Space* and *Account* parameters can be provided via special command line flags (*--token*, *--space*,  
and *--account* respectively) but can be conveniently placed in a config file relative to your user folder,
so they don't need to be provided each time.

The config file can be easily created and managed using the interactive `torque configure` command.
The CLI supports multiple profiles and we recommend setting up a default profile for ease of use. To use a non-default profile the _--profile_ command line flag needs to be used to specify the profile name.

To add a new profile or update an existing one run ```torque configure set``` and follow the on-screen directions. First you will be able to choose the profile name. Hit enter to add/update the default profile or enter a custom profile name. If the profile exists it will be update and if it doesn't exist then a new profile will be configured.
If you want to generate token by Torque CLI then use the ```--login|-l``` option (does not work for SSO). You will be requested to enter email and password instead of token

To see all profiles run ```torque configure list``` and the command will output a table of all the profiles that are currently configured. Example output:
```bash
Profile Name    Torque Account    Space Name           Token
--------------  ----------------  -------------------  -------------
default         torque-demo       promotions-manager   *********jhtU
custom-profile  my-torque         my-space             *********igEw
```

If a profile is no longer needed it can be easily removed by running ```torque configure remove [profile-name]```

The `torque configure` command will save the config file relative to your home user directory ('~/.torque/config' on Mac and Linux or in '%UserProfile%\\.torque\\config' on Windows).
If you wish to place the config file in a different location, you can specify that location via an environment variable:

`$ export TORQUE_CONFIG_PATH=/path/to/file`

The different parameters may also be provided as environment variables instead of using the config file:

```bash
export TORQUE_TOKEN = xxxzzzyyy
export TORQUE_SPACE = demo_space
# Optional
export TORQUE_ACCOUNT = MYACCOUNT
```

### Additional environment variables

It is possible to switch the client to different Torque instance setting custom API endpoint:

```bash
export TORQUE_HOSTNAME = "torque.example.com"
```


## Basic Usage

There are several basic actions Torque CLI currently allows you to perform:

- Validate a Blueprint (using the `torque bp validate` command)
- Get a list of blueprints (via `torque bp list`)
- Start an Environment (via `torque env start`)

In order to get help run:

`$ torque --help`

It will give you detailed output with usage:

```bash
$ torque --help
Usage: torque [--space=<space>] [--token=<token>] [--account=<account>] [--profile=<profile>] [--help] [--debug] [--disable-version-check]
              <command> [<args>...]

Options:
  -h --help             Show this screen.
  --version             Show current version
  --space=<space>       Use a specific Torque Space, this will override any default set in the config file
  --token=<token>       Use a specific token for authentication, this will override any default set in the
                        config file
  --account=<account>   [Optional] Your Torque account name.
  --profile=<profile>   Use a specific Profile section in the config file
                        You still can override config with --token/--space options.

Commands:
    bp, blueprint       validate torque blueprints
    env, environment    start environment, end environment and get its status
    configure           set, list and remove connection profiles to torque

```

You can get additional help information for a particular command by specifying *--help* flag after command name, like:

```torque sb --help
    usage:
        torque (env | environment) start <blueprint_name> [options]
        torque (env | environment) status <environment_id>
        torque (env | environment) end <environment_id>
        torque (env | environment) list [--filter={all|my|auto}] [--show-ended] [--count=<N>]
        torque (env | environment) [--help]

    options:
       -h --help                        Show this message

       -d, --duration <minutes>         The Environment will automatically de-provision at the end of the provided
                                        duration.
       
       -n, --name <environment_name>    Provide a name for the Environment. If not set, the name will be generated
                                        automatically using the source branch (or local changes) and current time.

       -i, --inputs <input_params>      The Blueprints inputs can be provided as a comma-separated list of key=value
                                        pairs. For example: key1=value1,key2=value2.
                                        By default Torque CLI will try to take the default values for these inputs
                                        from the Blueprint definition yaml file.

       -b, --branch <branch>            Run the Blueprint version from a remote Git branch. If not provided,
                                        the CLI will attempt to automatically detect the current working branch.
                                        The CLI will automatically run any local uncommitted or untracked changes in a
                                        temporary branch created for the validation or for the development Environment.

       -c, --commit <commitId>          Specify a specific Commit ID. This is used in order to run an Environment from a
                                        specific Blueprint historic version. If this parameter is used, the
                                        Branch parameter must also be specified.

       -t, --timeout <minutes>          Set how long (default timeout is 30 minutes) to block and wait before releasing
                                        control back to shell prompt. If timeout is reached before the desired status
                                        the wait loop will be interrupted.
                                        If "wait_active" flag is not set and a temp branch is created for local changes,
                                        the CLI will block and wait until the Environment Infrastructure is ready. Then 
                                        the temp branch can be safely deleted and the wait loop will end. 
                                        If "wait_active" flag is set, the CLI will block and wait until the Environment
                                        is Active regardless if temp branch is created or not.
                                        
       -w, --wait_active                Block shell prompt and wait for the Environment to be Active (or deployment
                                        ended with an error) while the timeout is not reached. Default timeout
                                        is 30 minutes. The default timeout can be changed using the "timeout" flag.
```

### Blueprint validation

Specify a file containing the declaration of your blueprint using the following command:

`$ torque bp validate MyBlueprint.yaml`

If blueprint has any errors you will see them printed:

```bash
message                                                                   name                  code
------------------------------------------------------------------------  --------------------  ----------------------
Value '{{.grains.OracleInstance.outputs.instance_id}}' can't be resolved  Value does not exist  VALUE_CANT_BE_RESOLVED
```

The Torque CLI can also read the a blueprint content from stdin. In this case, you need to provide a dash "-" instead
of a path to the file.

### Testing local changes

The Torque CLI can validate your Blueprints and test your Environments even before you commit and push your code to a
remote branch. It does so by creating a temporary branch on the remote repository with your local staged and even
untracked changes which gets deleted automatically after the Environment is created or the Blueprint validation is
complete. The CLI will automatically detect if you have some local changes and use them unless you explicitly
set the --branch flag.

Please notice that in order to create an Environment from your local changes, the CLI must make sure they are
picked up by the Environment setup process before completing the action and deleting the temporary branch. This means
that when you launch a local Environment the CLI command will not return immediately. You'll also receive a warning
not to abort the wait as that might not give Torque enough time to pull your changes and the Environment may fail.
Feel free to launch the CLI command asynchronously or continue working in a new tab.

---
**NOTE**

If you are not it git-enabled folder of your Blueprint repo and haven't set --branch/--commit arguments tool will
validate Blueprint with name "MyBlueprint" from branch currently attached to your Torque space.

---

The result will indicate whether the Blueprint is valid. If there are ny issues, you will see them printed out as
a table describing each issue found.

**Example:**

```bash
$ torque blueprint validate Jenkins -b master

ERROR - torque.commands - Validation failed
message                                                                      name
---------------------------------------------------------------------------  -------------------------------
Cloud account: AWS is not recognized as a valid cloud account in this space  Blueprint unknown cloud account
```

### Launching an Environment

* Similar to the previous command you can omit *--branch/--commit* arguments if you are in a git-enabled folder of your
  Blueprint repo:

    `$ torque env start MyBlueprint`

* This will create an Environment from the specified Blueprint

* If you want to start an Environment from a Blueprint in a specific state, specify _--branch_ and _--commit_ arguments:

    `$ torque env start MyBlueprint --branch dev --commit fb88a5e3275q5d54697cff82a160a29885dfed24`

* Additional optional options that you can provide here are:
  * `-d, --duration <minutes>` - you can specify duration for the Environment in minutes. Default is 120 minutes
  * `-n, --name <environment_name>` - the name of the Environment you want to create. By default, the cli will generate a name using the Blueprint name, branch or local changes, and the current timestamp
  * `-i, --inputs <input_params>` - comma-separated list of input parameters for the Environment, For example:_"param1=val1, param2=val2_"
  * `-w, --wait <timeout>` - <timeout> is a number of minutes. If set, you Torque CLI will wait for the Environment to become active and lock your terminal.
---
**NOTE**

1. If you are not it git-enabled folder of your Blueprint repo and haven't set --branch/--commit arguments tool will
start an Environment using the Blueprint "MyBlueprint" from the branch currently attached to your Torque space.

2. If you omit inputs options, you are inside a git enabled folder and the local is in sync with remote,
then Torque Cli will try to get default values for inputs from the Blueprint YAML file.
---

Result of the command is an Environment ID.

**Example**:

```bash
$ torque env start MyBlueprint --inputs "CS_TORQUE_TOKEN=ABCD, IAM_ROLE=s3access-profile, BUCKET_NAME=abc"

ybufpamyok03c11
```

### Other functionality

You can also end a Torque Environment by using the "end" command and specifying its Id:

`$ torque env end <environment_id>`

To get the current status of an Environment status run:

`$ torque env status <environment_id>`

In order to list all Environments in your space use the following command:

`$ torque env list`

- By default, this command will show only Environments launched by the CLI user which are not in an ended status.
- You can include historic completed Environments by setting `--show-ended` flag
- Default output length is 25. You can override with option `--count=N` where N < 1000
- You can also list Environments created by other users or filter only automation Environments by setting option
`--filter={all|my|auto}`. Default is `my`.

## Troubleshooting and Help

To troubleshoot what Torque CLI is doing you can add _--debug_ to get additional information.

For questions, bug reports or feature requests, please refer to the [Issue Tracker](https://github.com/QualiTorque/torque-cli/issues).


## Contributing


All your contributions are welcomed and encouraged. We've compiled detailed information about:

* [Contributing](.github/contributing.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)
