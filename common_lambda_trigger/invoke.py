"""
    A prefect flow & deployment used for invoking lambda functions on AWS.
"""
import json
import boto3
from prefect import flow


@flow(
    name="common-lambda-trigger",
    description="A flow for invoking lambda functions on AWS.",
    version="v1.0.0",
    retries=2,
    retry_delay_seconds=10,
    timeout_seconds=20,
)
def invoke_lambda_function(
    function_name: str,
    payload: str = json.dumps({}),
    invocation_type: str = "Event",
):
    """A flow for invoking lambda functions by name on AWS.

    Parameters
    ----------
    function_name: str
        The name of the lambda function to invoke.

    payload: str, optional (default=json.dumps({}))
        The payload to send to the lambda function.

    invocation_type: InvocationType, optional (default="Event")
        The invocation type of the lambda function.

    Returns
    -------
    dict:
        The response from the lambda function.
    """
    try:
        lambda_client = boto3.client("lambda")
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=payload,
        )
        return response

    except Exception as e:
        raise e
