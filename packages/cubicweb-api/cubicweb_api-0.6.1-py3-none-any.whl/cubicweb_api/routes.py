# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from contextlib import contextmanager
from enum import Enum
from typing import Callable

from cubicweb import AuthenticationError, QueryError, Unauthorized, Forbidden
from cubicweb.pyramid.core import CubicWebPyramidRequest
from cubicweb.schema_exporters import JSONSchemaExporter
from rql import RQLException
from yams import ValidationError, UnknownType
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPError
import logging

from cubicweb_api.api_transaction import ApiTransactionsRepository
from cubicweb_api.constants import (
    DEFAULT_ROUTE_PARAMS,
    API_ROUTE_NAME_PREFIX,
)
from cubicweb_api.httperrors import get_http_error, get_http_500_error
from cubicweb_api.auth.jwt_auth import setup_jwt
from cubicweb_api.openapi.openapi import setup_openapi
from cubicweb_api.util import get_cw_repo, get_transactions_repository

log = logging.getLogger(__name__)


class ApiRoutes(str, Enum):
    """
    All the available routes as listed in the openapi/openapi_template.yml file.
    """

    schema = "schema"
    rql = "rql"
    login = "login"
    transaction_begin = "transaction/begin"
    transaction_execute = "transaction/execute"
    transaction_commit = "transaction/commit"
    transaction_rollback = "transaction/rollback"
    help = "help"


def is_user_allowed(request: Request):
    """
    Checks if the user making the request is authenticated or if anonymous access is enabled

    :param request: The request initiated by the user
    :return: True if the user can access the resource, false otherwise
    """
    return (
        request.authenticated_userid is not None
        or get_cw_repo(request).config["anonymous-user"] is not None
    )


def get_route_name(route_name: str) -> str:
    """
    Generates a unique route name using the api prefix to prevent clashes with routes
    from other cubes.

    :param route_name: The route name base
    :return: The generated route name
    """
    return f"{API_ROUTE_NAME_PREFIX}{route_name}"


@contextmanager
def _catch_rql_errors(cw_req: CubicWebPyramidRequest):
    """
    Calls and returns the result of the given function.
    If an error related to RQL occurs, this will raise an HTTP 400 error

    :param func: The function to check for errors
    :return: The function's result if no error occurred
    :raise HTTPError: with 400 code if a RQL related exception is caught
    """
    try:
        try:
            yield
        except ValidationError as e:
            e.translate(cw_req._)
            raise
    except (RQLException, QueryError, ValidationError, UnknownType) as e:
        log.info(e.__class__.__name__, exc_info=True)
        raise get_http_error(400, e.__class__.__name__, str(e))


def view_exception_handler(func: Callable):
    """
    Use it as a decorator for any pyramid view to catch authentication errors
    and raise HTTP 401 or 403 errors.
    It also catches any other leftover exceptions and raises an HTTP 500 error.

    :param func: The pyramid view function
    :raise HTTPError: with different error codes depending on the exception caught
    """

    def request_wrapper(request: Request):
        try:
            return func(request)
        except HTTPError as e:
            # The decorated function raised its own HTTP error, simply forward it.
            return e
        except (AuthenticationError, Unauthorized) as e:
            # User was not authenticated, return 401 HTTP error
            log.info(e.__class__.__name__, exc_info=True)
            return get_http_error(401, e.__class__.__name__, str(e))
        except Forbidden as e:
            # User was authenticated but had insufficient privileges, return 403 HTTP error
            log.info(e.__class__.__name__, exc_info=True)
            return get_http_error(403, e.__class__.__name__, str(e))
        except Exception:
            # An exception was raised but not caught, this is a server error (HTTP 5OO)
            log.info("ServerError", exc_info=True)
            raise get_http_500_error()

    return request_wrapper


def authorized_users_only(func: Callable):
    """
    Use it as a decorator to raise an AuthenticationError if no user is detected
    and anonymous access is disabled.

    :param func: The pyramid view function
    """

    def request_wrapper(request: Request):
        if is_user_allowed(request):
            return func(request)
        raise AuthenticationError

    return request_wrapper


@view_config(
    route_name=get_route_name(ApiRoutes.schema),
    **dict(DEFAULT_ROUTE_PARAMS, request_method="GET"),
)
@view_exception_handler
@authorized_users_only
def schema_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    repo = get_cw_repo(request)
    exporter = JSONSchemaExporter()
    exported_schema = exporter.export_as_dict(repo.schema)
    return exported_schema


@view_config(
    route_name=get_route_name(ApiRoutes.rql),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
@authorized_users_only
def rql_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    request_params = request.openapi_validated.body
    query: str = request_params["query"]
    params: dict = request_params["params"]
    with _catch_rql_errors(request.cw_cnx):
        return request.cw_cnx.execute(query, params).rows


@view_config(
    route_name=get_route_name(ApiRoutes.login),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
def login_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    request_params = request.openapi_validated.body
    login: str = request_params["login"]
    pwd: str = request_params["password"]

    repo = get_cw_repo(request)
    with repo.internal_cnx() as cnx:
        try:
            cwuser = repo.authenticate_user(cnx, login, password=pwd)
        except AuthenticationError:
            raise get_http_error(
                401, "AuthenticationFailure", "Login and/or password invalid."
            )
        else:
            headers = request.authentication_policy.remember(
                request,
                cwuser.eid,
                login=cwuser.login,
                firstname=cwuser.firstname,
                lastname=cwuser.surname,
            )
            return Response(headers=headers, status=204)


@view_config(
    route_name=get_route_name(ApiRoutes.transaction_begin),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
@authorized_users_only
def transaction_begin_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    transactions = get_transactions_repository(request)
    user = request.cw_cnx.user
    return transactions.begin_transaction(user)


@view_config(
    route_name=get_route_name(ApiRoutes.transaction_execute),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
@authorized_users_only
def transaction_execute_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    transactions = get_transactions_repository(request)
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    query: str = request_params["query"]
    params: dict = request_params["params"]
    with _catch_rql_errors(request.cw_cnx):
        return transactions[uuid].execute(query, params).rows


@view_config(
    route_name=get_route_name(ApiRoutes.transaction_commit),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
@authorized_users_only
def transaction_commit_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    transactions = get_transactions_repository(request)
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    with _catch_rql_errors(request.cw_cnx):
        return transactions[uuid].commit()


@view_config(
    route_name=get_route_name(ApiRoutes.transaction_rollback),
    **DEFAULT_ROUTE_PARAMS,
)
@view_exception_handler
@authorized_users_only
def transaction_rollback_route(request: Request):
    """
    See the openapi/openapi_template.yml file for more information on this route.
    """
    transactions = get_transactions_repository(request)
    request_params = request.openapi_validated.body
    uuid: str = request_params["uuid"]
    rollback_result = transactions[uuid].rollback()
    transactions.end_transaction(uuid)
    return rollback_result


def includeme(config: Configurator):
    setup_jwt(config)
    repo = get_cw_repo(config)
    repo.api_transactions = ApiTransactionsRepository(repo)
    setup_openapi(config)
    config.pyramid_openapi3_register_routes()
    config.scan()
