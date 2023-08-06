"""Collection of exceptions for the SecretAccessor class."""


class SecretsAssessorError(Exception):
    """Generic exception for any error in Secrets Accessor"""
    pass


class GCPCredentialError(SecretsAssessorError):
    """Raised when the credential file is not found or is invalid."""
    pass


class SecretNotFoundError(SecretsAssessorError):
    """Exception raised when secret is not found."""
    pass

