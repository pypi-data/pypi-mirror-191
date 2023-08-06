import logging

import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import COMMAND_CLS, ENABLE_CLUSTER_COMMANDS, GROUP_CLS
from servicefoundry.cli.display_util import print_entity_obj, print_json, print_obj
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.dao import application as application_lib
from servicefoundry.lib.dao import version as version_lib
from servicefoundry.lib.dao import workspace as workspace_lib
from servicefoundry.lib.model.entity import Cluster

logger = logging.getLogger(__name__)

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="get", cls=GROUP_CLS)
def get_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Get servicefoundry resources

    \b
    Supported resources:
    - Workspace
    - Service
    - Deployment
    """
    pass


@click.command(name="cluster", cls=COMMAND_CLS, help="Get Cluster metadata")
@click.argument("cluster_id")
@handle_exception_wrapper
def get_cluster(cluster_id):
    tfs_client = ServiceFoundryServiceClient()
    cluster = tfs_client.get_cluster(cluster_id)
    if CliConfig.get("json"):
        print_json(data=cluster)
    else:
        print_obj("Cluster", cluster, columns=Cluster.get_display_columns)


@click.command(name="workspace", cls=COMMAND_CLS, help="Get Workspace metadata")
@click.option(
    "-w",
    "--workspace-fqn",
    type=click.STRING,
    default=None,
    help="workspace fqn",
    required=True,
)
@handle_exception_wrapper
def get_workspace(workspace_fqn):
    workspace = workspace_lib.get_workspace_by_fqn(workspace_fqn=workspace_fqn)
    if CliConfig.get("json"):
        print_json(data=workspace.to_dict())
    else:
        print_entity_obj("Workspace", workspace)


@click.command(name="application", cls=COMMAND_CLS, help="Get Application metadata")
@click.option(
    "--application-fqn",
    type=click.STRING,
    default=None,
    help="application fqn",
    required=True,
)
@handle_exception_wrapper
def get_application(application_fqn):
    application = application_lib.get_application(application_fqn=application_fqn)
    if CliConfig.get("json"):
        print_json(data=application.to_dict())
    else:
        print_entity_obj(
            "Application",
            application,
        )


@click.command(
    name="application-version", cls=COMMAND_CLS, help="Get Application Version metadata"
)
@click.option(
    "--application-fqn",
    type=click.STRING,
    default=None,
    help="application fqn",
    required=True,
)
@click.option(
    "--version",
    type=click.STRING,
    default=None,
    help="application version",
    required=True,
)
@handle_exception_wrapper
def get_version(application_fqn, version):
    version = version_lib.get_version(application_fqn=application_fqn, version=version)
    if CliConfig.get("json"):
        print_json(data=version.to_dict())
    else:
        print_entity_obj("Version", version)


def get_get_command():
    get_command.add_command(get_workspace)
    get_command.add_command(get_application)
    get_command.add_command(get_version)
    # get_command.add_command(get_current_context)
    # get_command.add_command(get_logs)

    if ENABLE_CLUSTER_COMMANDS:
        get_command.add_command(get_cluster)
    return get_command
