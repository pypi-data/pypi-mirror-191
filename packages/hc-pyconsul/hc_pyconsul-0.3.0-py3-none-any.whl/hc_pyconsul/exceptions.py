class UnaAuthorized(Exception):
    """Raised when Consul returns a 401."""
    pass


class UnknownResourceCalled(Exception):
    pass


class Unauthenticated(Exception):
    pass
