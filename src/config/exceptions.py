from typing import Optional

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def drf_exception_handler(exc, context):
    exception_handler(exc, context)

    if isinstance(exc, TyiynBadRequest):
        return Response(
            {"code": exc.code, "message": exc.message, "field_errors": []},
            status=exc.http_code,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                "code": TyiynUnauthorized.code,
                "message": TyiynUnauthorized.message,
                "error_fields": [],
            },
            status=TyiynUnauthorized.http_code,
        )

    if isinstance(exc, AuthenticationFailed):
        return Response(
            {
                "code": TyiynAuthenticationFailed.code,
                "message": TyiynAuthenticationFailed.message,
                "error_fields": [],
            },
            status=TyiynAuthenticationFailed.http_code,
        )

    if isinstance(exc, APIException):
        try:
            return Response(
                {
                    "code": TyiynBadRequest.code,
                    "message": TyiynBadRequest.message,
                    "field_errors": [
                        {
                            "field": field,
                            "message": message if type(message) is dict else message[0],
                        }
                        for field, message in zip(exc.detail, exc.detail.values())
                    ],
                },
                status=exc.status_code,
            )

        except Exception as e:  # noqa F841
            return Response(
                {
                    "code": TyiynBadRequest.code,
                    "message": str(exc),
                    "field_errors": [],
                },
                status=exc.status_code,
            )

    if isinstance(exc, Http404):
        return Response(
            {
                "code": TyiynNotFound.code,
                "message": TyiynNotFound.message,
                "error_fields": [],
            },
            status=TyiynNotFound.http_code,
        )

    return None


class TyiynBaseException(Exception):
    code = "UnexpectedException"
    message = "Unexpected error occurred while processing your request"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    field_errors: list = []

    def __init__(
        self,
        message: str = "",
        code: str = "",
        http_code: Optional[int] = None,
        field_errors: Optional[list] = None,
    ):
        self.code = code or self.code
        self.message = message or self.message
        self.http_code = http_code or self.http_code
        self.field_errors = field_errors or self.field_errors


class TyiynNotFound(TyiynBaseException):
    code = "ObjectDoesNotExist"
    message = "Object does not exist"
    http_code = status.HTTP_404_NOT_FOUND


class TyiynBadRequest(TyiynBaseException):
    code = "BadRequest"
    message = "Invalid request, please try again later"
    http_code = status.HTTP_400_BAD_REQUEST


class TyiynPermissionDenied(TyiynBaseException):
    code = "PermissionDenied"
    message = "Permission Denied"
    http_code = status.HTTP_403_FORBIDDEN


class TyiynUnauthorized(TyiynBaseException):
    code = "Unauthorized"
    message = "Unauthorized"
    http_code = status.HTTP_401_UNAUTHORIZED


class TyiynAuthenticationFailed(TyiynUnauthorized):
    code = "AuthenticationError"
    message = "Authentication Error"
    http_code = status.HTTP_401_UNAUTHORIZED
