"""Bounded public-source adapter failures."""


class DataSourceError(Exception):
    """Base class for expected external data-source failures."""


class SourceNotFoundError(DataSourceError):
    """The requested public reference does not exist."""


class SourceTemporarilyUnavailableError(DataSourceError):
    """The source rejected or could not serve a retryable request."""


class SourceResponseInvalidError(DataSourceError):
    """The source returned an unexpected, unsafe, or oversized response."""
