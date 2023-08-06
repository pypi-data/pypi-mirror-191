import sys
from typing import TYPE_CHECKING

import boto3
import logging
from botocore.exceptions import ClientError, ProfileNotFound

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Type

    from boto3 import Session
    from boto3.resources.base import ServiceResource


class AWSConnector:
    """
    AWSConnector - Connects to AWS using Credentials File or IAM Role
    """

    @staticmethod
    def __get_assumed_role_credentials(aws_role_to_assume: str) -> "Dict[str, str]":
        """
        __get_assumed_role_credentials
            :param aws_role_to_assume: the arn of an AWS role to assume
            :return:
        """
        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=aws_role_to_assume,
            RoleSessionName=f"{__class__.__name__}-session",  # type: ignore[name-defined]
        )
        return assumed_role_object["Credentials"]

    @staticmethod
    def __create_boto_3_session(
        profile_name: "Optional[str]",
        aws_role_to_assume: "Optional[str]" = None,
    ) -> "Optional[Session]":
        """
        __create_boto_3_session
            :param profile_name:
            :param aws_role_to_assume: (Optional) the arn of an AWS role to assume
            :return:
        """
        current_class_name = __class__.__name__  # type: ignore[name-defined]
        logger = logging.getLogger(current_class_name)

        try:
            if aws_role_to_assume:
                # TRYING TO ASSUME A SPECIFIC ROLE USING DEFAULT CREDENTIALS
                try:
                    temporary_credentials = AWSConnector.__get_assumed_role_credentials(
                        aws_role_to_assume=aws_role_to_assume
                    )
                    session = boto3.Session(
                        aws_access_key_id=temporary_credentials["AccessKeyId"],
                        aws_secret_access_key=temporary_credentials["SecretAccessKey"],
                        aws_session_token=temporary_credentials["SessionToken"],
                    )
                    return session
                except Exception as noCredentialsErrorException:
                    logger.warning(
                        f"[{current_class_name}] - Default Profile/IAM Role Could not assume "
                        f"{aws_role_to_assume} role. This is not an expected behavior."
                        f"{str(noCredentialsErrorException)}"
                    )
            try:
                if profile_name and boto3.session.Session(profile_name=profile_name).get_credentials():
                    # TRY USING A SPECIFIC PROFILE_NAME (USING A CREDENTIALS FILE)
                    logger.info("Trying to connect to AWS using Credentials File with profile_name: " + profile_name)

                    session = boto3.Session(profile_name=profile_name)
                    return session

            except ProfileNotFound as profileNotFoundException:
                logger.debug(
                    "["
                    + current_class_name
                    + "] - Could not find profile name - Trying using Default Profile/IAM Role"
                    + str(profileNotFoundException)
                )

            # TRY USING AN IAM ROLE (OR *DEFAULT* CREDENTIALS - USING A CREDENTIALS FILE)
            logger.info("Trying to connect to AWS using IAM role or Default Credentials")
            session = boto3.Session()
            return session

        except Exception as ex:
            logger.critical(
                "["
                + current_class_name
                + "] - Caught Exception while trying to connect to AWS Credentials Manager "
                + str(ex)
            )
            return None

    @staticmethod
    def get_aws_session(
        profile_name: "Optional[str]",
        aws_role_to_assume: "Optional[str]" = None,
    ) -> "Optional[Session]":
        """
        get_aws_session - Connects to AWS to retrieve an AWS Session
            :param      profile_name: The Config Profile (Environment Name in Credentials file)
            :param      aws_role_to_assume: (Optional) the arn of an AWS role to assume
            :return:    boto3 Session
        """
        current_class_name = __class__.__name__  # type: ignore[name-defined]
        logger = logging.getLogger(current_class_name)

        aws_session = AWSConnector.__create_boto_3_session(
            profile_name=profile_name,
            aws_role_to_assume=aws_role_to_assume,
        )
        if aws_session is None:
            logger.error("Failed to initiate an AWS Session")

        return aws_session

    @staticmethod
    def get_aws_client_for_service_name(
        profile_name: "Optional[str]",
        service_name: str,
        aws_role_to_assume: "Optional[str]" = None,
    ) -> "Any":
        """
        get_aws_client_for_service_name - Connects to AWS to retrieve the relevant Client
            :param      profile_name: The Config Profile (Environment Name in Credentials file)
            :param      service_name: The AWS Service name to get the Client for
            :param      aws_role_to_assume: (Optional) the arn of an AWS role to assume
            :return:    Service client instance
        """
        current_class_name = __class__.__name__  # type: ignore[name-defined]
        logger = logging.getLogger(current_class_name)

        aws_session = AWSConnector.__create_boto_3_session(
            profile_name=profile_name, aws_role_to_assume=aws_role_to_assume
        )
        if aws_session is None:
            logger.error("Failed to connect to AWS client: " + str(service_name))
            return None

        return aws_session.client(service_name=service_name)  # type: ignore[call-overload]

    @staticmethod
    def get_aws_resource_for_service_name(
        profile_name: "Optional[str]",
        service_name: str,
        aws_role_to_assume: "Optional[str]" = None,
    ) -> "Optional[ServiceResource]":
        """
        Connects to AWS to retrieve the relevant Resource (More functionality then Client)
            :param      profile_name: The Config Profile (Environment Name in Credentials file)
            :param      service_name: The AWS Service name to get the Client for
            :param      aws_role_to_assume: (Optional) the arn of an AWS role to assume
            :return:    Service client instance
        """
        current_class_name = __class__.__name__  # type: ignore[name-defined]
        logger = logging.getLogger(current_class_name)

        aws_session = AWSConnector.__create_boto_3_session(
            profile_name=profile_name, aws_role_to_assume=aws_role_to_assume
        )
        if aws_session is None:
            logger.error("Failed to connect to AWS client: " + str(service_name))
            return None

        return aws_session.resource(service_name=service_name)  # type: ignore[call-overload]

    @staticmethod
    def is_client_error(code: str) -> "Type[Exception]":
        e = sys.exc_info()[1]
        if isinstance(e, ClientError) and e.response["Error"]["Code"] == code:
            return ClientError
        return type("NeverEverRaisedException", (Exception,), {})
