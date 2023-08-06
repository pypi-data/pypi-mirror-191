import logging
from datetime import datetime
from typing import Optional

import rich_click as click
from dateutil.tz import tzlocal

from servicefoundry.cli.const import COMMAND_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.io.rich_output_callback import RichOutputCallBack
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.logs_utils import get_timestamp_from_timestamp_or_duration

logger = logging.getLogger(__name__)


@click.command(name="logs", cls=COMMAND_CLS)
@click.option(
    "--application-fqn", type=click.STRING, help="application fqn", required=True
)
@click.option("--version", type=click.INT, help="deployment version", default=None)
@click.option(
    "--since",
    type=click.STRING,
    help="Show logs since timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)",
    default="2h",
)
@click.option(
    "--until",
    type=click.STRING,
    help="Show logs until timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)",
    default=None,
)
@click.option(
    "-n", "--tail", type=click.INT, help="Number of logs to tail", default=None
)
@handle_exception_wrapper
def logs_command(
    application_fqn: str,
    version: Optional[int],
    since: str,
    until: Optional[str],
    tail: Optional[int],
) -> None:
    """
    Get log tails for application fqn
    """
    start_ts = get_timestamp_from_timestamp_or_duration(since)
    end_ts = (
        get_timestamp_from_timestamp_or_duration(until)
        if until
        else datetime.now().timestamp() * 1000
    )

    output_hook = RichOutputCallBack()
    tfs_client = ServiceFoundryServiceClient()

    if version:
        deployment_fqn_response = tfs_client.get_deployment_info_by_fqn(
            f"{application_fqn}:{version}"
        )
        workspace_id, application_id, deployment_id = (
            deployment_fqn_response.workspaceId,
            deployment_fqn_response.applicationId,
            deployment_fqn_response.deploymentId,
        )
    else:
        app_fqn_response = tfs_client.get_application_info_by_fqn(application_fqn)
        workspace_id, application_id, deployment_id = (
            app_fqn_response.workspaceId,
            app_fqn_response.applicationId,
            None,
        )

    logger.info(
        "Fetching logs from %s to %s for application fqn: %s",
        datetime.fromtimestamp(start_ts / 1000, tzlocal()).isoformat(),
        datetime.fromtimestamp(end_ts / 1000, tzlocal()).isoformat(),
        application_fqn,
    )

    tfs_client.fetch_deployment_logs(
        workspace_id=workspace_id,
        application_id=application_id,
        deployment_id=deployment_id,
        start_ts=start_ts,
        end_ts=end_ts,
        limit=tail,
        callback=output_hook,
    )


def get_logs_command():
    return logs_command
