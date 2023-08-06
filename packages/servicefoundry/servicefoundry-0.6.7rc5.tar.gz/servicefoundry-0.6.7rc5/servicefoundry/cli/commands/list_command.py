import logging

import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.console import console
from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.display_util import print_entity_list, print_json, print_list
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.dao import application as application_lib
from servicefoundry.lib.dao import version as version_lib
from servicefoundry.lib.dao import workspace as workspace_lib
from servicefoundry.lib.messages import (
    PROMPT_NO_APPLICATIONS,
    PROMPT_NO_VERSIONS,
    PROMPT_NO_WORKSPACES,
)
from servicefoundry.lib.model.entity import Cluster

logger = logging.getLogger(__name__)

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="list", cls=GROUP_CLS)
def list_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry list resources
    """


@click.command(name="cluster", cls=COMMAND_CLS, help="List Clusters")
@handle_exception_wrapper
def list_cluster():
    tfs_client = ServiceFoundryServiceClient()
    clusters = tfs_client.list_cluster()
    if CliConfig.get("json"):
        print_json(data=clusters)
    else:
        print_entity_list("Clusters", clusters, Cluster.list_display_columns)


@click.command(name="workspaces", cls=COMMAND_CLS, help="List Workspaces")
@click.option(
    "-c", "--cluster-name", type=click.STRING, default=None, help="cluster name"
)
@handle_exception_wrapper
def list_workspaces(cluster_name):
    # Tests:
    # - Set Context -> list workspace -> Should get workspaces in set cluster
    # - Set Context -> list workspace -c 'cluster_name' -> Should get workspaces in given cluster
    # - Set Context -> list workspace -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - Set Context -> list workspace -A -> Should give all workspaces across all clusters
    # - No Context -> list workspace -c 'cluster_name' -> Should get workspaces in given cluster
    # - No Context -> list workspace -c 'invalid_cluster_name' -> Should give error invalid cluster
    # - No Context -> list workspace -A -> Should give all workspaces across all clusters
    # ? No Context -> list workspace -> Should list workspaces if there is only cluster or ask for cluster name
    workspaces = workspace_lib.list_workspaces(
        cluster_name=cluster_name,
    )
    if not workspaces:
        console.print(PROMPT_NO_WORKSPACES)
    else:
        workspaces.sort(key=lambda s: (s.createdAt), reverse=True)

    if CliConfig.get("json"):
        print_json(data=workspaces)
    else:
        print_entity_list(
            "Workspaces",
            workspaces,
        )


@click.command(name="applications", cls=COMMAND_CLS, help="List Applications")
@click.option(
    "-w", "--workspace-fqn", type=click.STRING, default=None, help="workspace fqn"
)
@click.option(
    "--application-type",
    type=click.Choice(["job", "model-deployment", "service", "all"]),
    default="all",
    help="application type",
)
@handle_exception_wrapper
def list_applications(workspace_fqn, application_type):
    applications = application_lib.list_applications(
        workspace_fqn=workspace_fqn, application_type=application_type
    )
    if not applications:
        console.print(PROMPT_NO_APPLICATIONS)
    else:
        applications.sort(key=lambda s: (s.createdAt), reverse=True)
    if CliConfig.get("json"):
        print_json(data=applications)
    else:
        # TODO (chiragjn): Display columns here need to show workspace and cluster name!
        print_entity_list(
            "Applications",
            applications,
        )


@click.command(
    name="application-versions", cls=COMMAND_CLS, help="List Application Versions"
)
@click.option(
    "--application-fqn",
    type=click.STRING,
    default=None,
    help="application fqn",
    required=True,
)
@handle_exception_wrapper
def list_versions(application_fqn):
    versions = version_lib.list_versions(
        application_fqn=application_fqn,
    )
    if not versions:
        console.print(PROMPT_NO_VERSIONS)
    else:
        versions.sort(key=lambda s: (s.createdAt), reverse=True)
    if CliConfig.get("json"):
        print_json(data=versions)
    else:
        # TODO (chiragjn): Display columns here need to show workspace and cluster name!
        print_entity_list(
            "Application Versions",
            versions,
        )


@click.command(
    name="authorize", cls=COMMAND_CLS, help="List authorization for a resource id."
)
@click.argument("resource_type", type=click.Choice(["workspace"], case_sensitive=False))
@click.argument("resource_id")
@handle_exception_wrapper
def list_authorize(resource_type, resource_id):
    tfs_client = ServiceFoundryServiceClient()
    response = tfs_client.get_authorization_for_resource(resource_type, resource_id)
    print_list(f"Auth for {resource_type}: {resource_id}", response)


def get_list_command():
    list_command.add_command(list_workspaces)
    list_command.add_command(list_applications)
    list_command.add_command(list_versions)

    # if ENABLE_CLUSTER_COMMANDS:
    #     list_command.add_command(list_cluster)

    return list_command
