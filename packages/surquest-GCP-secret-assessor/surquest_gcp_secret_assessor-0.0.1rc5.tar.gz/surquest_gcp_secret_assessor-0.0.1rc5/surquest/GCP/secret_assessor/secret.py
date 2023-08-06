"""Secret module defines Secret class
that provides access to secrets stored in Google Cloud Platform Secret Manager
or mounted as environment variables.
"""
import os
import yaml
import json
from google.cloud import secretmanager
import google.auth
from google.api_core import exceptions

from .exceptions import (
    SecretNotFoundError
)


class Secret:
    """Secret class provides access to secrets stored in Google Cloud Platform
    Secret Manager or mounted as environment variables.
    """

    @classmethod
    def get(cls, name: str, parse="TXT", version: str = "latest") -> str:
        """Method returns secret value for a secret
        within Google Cloud Platform Secret Manager or mounted as environment.
        The secret is identified by the secret name.

        :param name: secret name / secret_id in GCP Secret Manager
        :type name: str

        :param parse: parse secret value as JSON|YAML or return as string
        :type parse: str

        :param version: secret version / version_id in GCP Secret Manager
        :type version: str
        """

        value = os.getenv(name)

        if value is not None:

            return value

        # Get secret value from Secret Manager client

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        project_id = cls.get_project_id()

        # Build the resource name of the secret version.
        path = client.secret_version_path(
            project=project_id,
            secret=name,
            secret_version=version
        )

        # Access the secret version.
        try:
            response = client.access_secret_version(name=path)

        except exceptions.PermissionDenied as e:

            raise SecretNotFoundError(str(e))

        # Return the decoded payload.
        value = response.payload.data.decode('UTF-8')

        if parse.upper() == "YAML":
            return yaml.loads(value, Loader=yaml.FullLoader)
        elif parse.upper() == "JSON":
            return json.loads(value)
        else:
            return value

    @classmethod
    def get_credentials(cls, credentials=None):
        """Method returns credentials object

        :param credentials: Google Cloud Credentials object
        :type credentials: service_account.Credentials
        :return: instance of Google Cloud Credentials
        :rtype: service_account.Credentials
        """

        # if credentials are not passed, get it from ENV variable
        if credentials is None:

            credentials, project_id = google.auth.default()

        return credentials

    @classmethod
    def get_project_id(cls):
        """Method returns GOOGLE_CLOUD_PROJECT

        Workflows:

            1. If GOOGLE_CLOUD_PROJECT environment variable is set, return it.
            2. If GOOGLE_APPLICATION_CREDENTIALS environment variable is set
            get PROJECT ID from it.

        :return: project id
        :rtype: str
        :raises: ProjectIdNotFoundError
        """

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

        if project_id is None:

            credentials, project_id = google.auth.default()

        return project_id



