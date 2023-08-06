# import external modules
import os
from google.oauth2 import service_account

# import internal modules
from surquest.GCP.secret_assessor import Secret, exceptions



class TestSecret:
    ERRORS = {
        "value": "Wrong value: Expected: `{}`, Actual: `{}`",
        "type": "Wrong type: Expected: `{}`, Actual: `{}`"
    }

    def test__get_secret__from_env_var(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from environment variable
        """

        secret_value = "This is a secret"
        os.environ["MY_SECRET"] = secret_value
        assert secret_value == Secret.get("MY_SECRET"), \
            self.ERRORS.get("value").format(
                secret_value,
                Secret.get("MY_SECRET")
            )

    def test__get_secret__from_gcp__success(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        secret_name = "dev--credentials--app-store"

        secret_value = Secret.get(secret_name)
        assert str == type(secret_value), \
            self.ERRORS.get("type").format(
                str,
                type(secret_value)
            )

    def test__get_secret__from_gcp__parse_json__success(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        secret_name = "dev--credentials--app-store"

        secret_value = Secret.get(secret_name, parse="JSON")
        assert dict == type(secret_value), \
            self.ERRORS.get("type").format(
                dict,
                type(secret_value)
            )

    def test__get_secret__from_gcp__error(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        secret_name = "unknown-secret"

        try:
            Secret.get(secret_name)
        except Exception as e:
            assert True is isinstance(e, exceptions.SecretsAssessorError)

    def test__get_credentials(self):
        """Method tests the get_credentials method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        credentials = Secret.get_credentials()

        assert True is isinstance(
            credentials,
            service_account.Credentials
        )



