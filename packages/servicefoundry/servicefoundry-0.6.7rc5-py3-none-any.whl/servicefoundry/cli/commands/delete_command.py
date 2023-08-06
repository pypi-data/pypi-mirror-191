import logging

import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.display_util import print_json
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.dao import application as application_lib
from servicefoundry.lib.dao import workspace as workspace_lib

logger = logging.getLogger(__name__)

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="delete", cls=GROUP_CLS)
def delete_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry delete resource

    \b
    Supported resources:
    - Workspace
    - Service
    """
    pass


@click.command(name="workspace", cls=COMMAND_CLS, help="Delete a Workspace")
@click.option(
    "-w",
    "--workspace-fqn",
    type=click.STRING,
    default=None,
    help="workspace fqn",
    required=True,
)
@click.confirmation_option(prompt="Are you sure you want to delete this workspace?")
@handle_exception_wrapper
def delete_workspace(workspace_fqn):
    deleted_workspace = workspace_lib.delete_workspace(
        workspace_fqn=workspace_fqn,
    )
    if CliConfig.get("json"):
        print_json(data=deleted_workspace.to_dict())


@click.command(name="application", cls=COMMAND_CLS, help="Delete an Application")
@click.option(
    "--application-fqn",
    type=click.STRING,
    default=None,
    help="application fqn",
    required=True,
)
@click.confirmation_option(prompt="Are you sure you want to delete this application?")
@handle_exception_wrapper
def delete_application(application_fqn):
    response = application_lib.delete_application(
        application_fqn=application_fqn,
    )
    if CliConfig.get("json"):
        print_json(data=response)


def get_delete_command():
    delete_command.add_command(delete_workspace)
    delete_command.add_command(delete_application)
    return delete_command
