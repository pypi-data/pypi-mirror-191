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
import re
from typing import Union

from cubicweb import ConfigurationError
from cubicweb.pyramid.config import AllInOneConfiguration
from cubicweb.server.repository import Repository
from pyramid.config import Configurator
from pyramid.request import Request

from cubicweb_api.api_transaction import ApiTransactionsRepository
from cubicweb_api.constants import API_PATH_DEFAULT_PREFIX


def get_cw_repo(req_or_conf: Union[Request, Configurator]) -> Repository:
    """
    Helper used to have typing on the CubicWeb repository.

    :param req_or_conf: A pyramid request or configurator object
    :return: A Repository object
    """
    return req_or_conf.registry["cubicweb.repository"]


def get_cw_all_in_one_config(config: Configurator) -> AllInOneConfiguration:
    """
    Helper used to have typing on the CubicWeb all in one configuration.

    :param config: A pyramid configurator object
    :return: A AllInOneConfiguration object
    """
    return config.registry["cubicweb.config"]


def get_transactions_repository(request: Request) -> ApiTransactionsRepository:
    """
    Helper used to have typing on the api transaction repository.

    :param request: The pyramid request containing the transaction repository
    :return: An ApiTransactionsRepository object
    """
    return get_cw_repo(request).api_transactions


def get_openapi_spec_server_url(config: Configurator) -> str:
    """
    Gets the server base url from the configuration.
    If no configuration is found, fallback to the CubicWeb base url

    :param config: A pyramid configurator object
    :return: The configured server name or the CubicWeb base url
    :raise ConfigurationError if the name set in config is not valid
    """
    cwconfig = get_cw_all_in_one_config(config)
    server_url: str = cwconfig.option_value("base-url")
    server_url += get_api_path_prefix(config)
    return server_url


def get_api_path_prefix(config: Configurator) -> str:
    """
    Gets the api path prefix from the configuration.
    If no configuration is found, fallback to the default api path prefix.

    :param config: A pyramid configurator object
    :return: The configured api path prefix or the default one
    :raise ConfigurationError: if the path set in config is not valid
    """
    repo = get_cw_repo(config)
    path_prefix: str = (
        repo.get_option_value("api-path-prefix") or API_PATH_DEFAULT_PREFIX
    ).strip("/")
    match = re.match("^[a-zA-Z0-9-_@.&+!*(),/]{1,29}$", path_prefix)
    if match:
        return f"{path_prefix}/v1"
    else:
        if len(path_prefix) > 30:
            raise ConfigurationError(
                f"api-path-prefix '{path_prefix}' is too long. "
                "Max size allowed is 30 characters. "
                f"Current size is {len(path_prefix)}."
            )

        raise ConfigurationError(
            f"api-path-prefix '{path_prefix}' contains invalid characters. "
            "Allowed characters are: a-zA-Z0-9-_@.&+!*(),/"
        )
