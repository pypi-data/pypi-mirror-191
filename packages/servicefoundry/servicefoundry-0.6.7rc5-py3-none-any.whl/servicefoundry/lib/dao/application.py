from typing import Any, Dict, Optional

import servicefoundry.lib.dao.version as version_lib
from servicefoundry.cli.console import console
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.model.entity import Deployment


def list_applications(
    application_type: str,
    workspace_fqn: Optional[str] = None,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient()
    if workspace_fqn:
        workspace = client.get_id_from_fqn(fqn=workspace_fqn, fqn_type="workspace")
        applications = client.list_applications(workspace_id=workspace["workspaceId"])
    else:
        applications = client.list_applications()

    if application_type != "all":
        applications = [
            application
            for application in applications
            if application.deployment.manifest.type == application_type
        ]
    return applications


def get_application(
    application_fqn: str,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient()
    application = client.get_id_from_fqn(fqn=application_fqn, fqn_type="app")
    application = client.get_application_info(
        application_id=application["applicationId"]
    )
    return application


def delete_application(
    application_fqn: str,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Dict[str, Any]:
    client = client or ServiceFoundryServiceClient()
    application = client.get_id_from_fqn(fqn=application_fqn, fqn_type="app")
    response = client.remove_application(application_id=application["applicationId"])

    console.print("""[yellow]Deleted Application[/]""")
    return response


def redeploy_application(
    application_fqn: str,
    version: int,
    wait: bool,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Deployment:
    from servicefoundry.v2 import Application

    client = client or ServiceFoundryServiceClient()

    deployment_info = version_lib.get_version(
        application_fqn=application_fqn, version=version
    )

    manifest = deployment_info.manifest.dict()

    application_id = deployment_info.applicationId
    application_info = client.get_application_info(application_id=application_id)
    workspace_fqn = application_info.workspace.fqn

    application = Application.parse_obj(manifest)
    deployment = application.deploy(workspace_fqn=workspace_fqn, wait=wait)
    return deployment
