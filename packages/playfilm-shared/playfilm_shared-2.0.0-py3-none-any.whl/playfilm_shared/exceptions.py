class MissingMetricInfoException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 541


class InvalidAccessTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 542


class GoogleApiException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 543


class MissingAccountIdException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 544


class MissingActionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 545


class MissingChannelException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 546


class QueryDBRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 547


class FacebookApiException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 548


class TikTokApiException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.code = 549
