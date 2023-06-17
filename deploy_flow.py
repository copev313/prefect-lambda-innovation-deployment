"""
    This file is used to set up the Prefect deployment for invoking lambda functions.
"""
from typing import Optional

from common_lambda_trigger.invoke import invoke_lambda_function
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.server.schemas.schedules import CronSchedule


def deploy(
    lambda_function_name: str,
    cron_schedule: str,
    tags: Optional[list] = None,
    version: Optional[str] = None,
    invocation_type: Optional[str] = None,
    payload: Optional[dict] = None,
):
    """Deploy the flow to Prefect Cloud."""
    try:
        # Load S3 Storage for flow deployment:
        s3_storage = S3.load("s3-deployments-block")

        # Build flow parameters to pass to the deployment:
        deployment_parameters = {
            "function_name": lambda_function_name,
        }
        if invocation_type:
            deployment_parameters["invocation_type"] = invocation_type
        if payload:
            deployment_parameters["payload"] = payload

        # Build the deployment configuration:
        deployment = Deployment.build_from_flow(
            flow=invoke_lambda_function,
            flow_name=f"{lambda_function_name}-flow",
            name=f"{lambda_function_name}-deployment",
            tags=tags if tags else ["common", "railway.app", "deployment"],
            version=version if version else "v1.0.0",
            storage=s3_storage,
            schedule=CronSchedule(cron=cron_schedule, timezone="America/New_York"),
            is_schedule_active=True,
            parameters=deployment_parameters,
        )
        deployment.apply()
        print("Deployment successful!")

    except Exception as e:
        raise e


if __name__ == "__main__":
    deploy(
        lambda_function_name="hello-world",
        cron_schedule="0 8 * * *",
    )
