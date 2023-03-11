from .constants import ErrorCode
from src import exceptions


class AuthRequired(exceptions.NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(exceptions.PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(exceptions.NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(exceptions.NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class EmailTaken(exceptions.BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN


class RefreshTokenNotValid(exceptions.NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID
