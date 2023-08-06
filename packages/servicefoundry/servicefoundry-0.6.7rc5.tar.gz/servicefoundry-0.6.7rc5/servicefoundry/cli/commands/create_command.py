import logging
from typing import Optional

import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.display_util import print_obj
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.dao import workspace as workspace_lib

logger = logging.getLogger(__name__)

WORKSPACE_DISPLAY_FIELDS = [
    "id",
    "name",
    "namespace",
    "status",
    "clusterId",
    "createdBy",
    "createdAt",
    "updatedAt",
]
DEPLOYMENT_DISPLAY_FIELDS = [
    "id",
    "serviceId",
    "domain",
    "deployedBy",
    "createdAt",
    "updatedAt",
]


@click.group(name="create", cls=GROUP_CLS)
def create_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Create servicefoundry resources

    \b
    Supported resources:
    - Workspace
    """
    pass


@click.command(name="workspace", cls=COMMAND_CLS, help="Create a new Workspace")
@click.argument("name", type=click.STRING)
@click.option(
    "-c",
    "--cluster-name",
    type=click.STRING,
    required=True,
    help="cluster to create this workspace in",
)
@click.option(
    "--cpu-limit",
    type=click.FLOAT,
    default=None,
    help="CPU Limit",
)
@click.option(
    "--memory-limit",
    type=click.INT,
    default=None,
    help="Memory Limit",
)
@click.option(
    "--ephemeral-storage-limit",
    type=click.INT,
    default=None,
    help="Ephemeral Storage Limit",
)
@handle_exception_wrapper
def create_workspace(
    name: str,
    cluster_name: str,
    cpu_limit: Optional[float],
    memory_limit: Optional[int],
    ephemeral_storage_limit: Optional[int],
):
    workspace = workspace_lib.create_workspace(
        name=name,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        ephemeral_storage_limit=ephemeral_storage_limit,
        cluster_name=cluster_name,
    )
    print_obj("Workspace", workspace.to_dict())


def get_create_command():
    create_command.add_command(create_workspace)
    return create_command
