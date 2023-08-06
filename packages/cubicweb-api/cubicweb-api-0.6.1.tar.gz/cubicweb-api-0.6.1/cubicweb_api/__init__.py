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
"""cubicweb-api application package

This cube is the new api which will be integrated in CubicWeb 4.
"""
from datetime import datetime, date, time
from typing import Union

from pyramid.config import Configurator
from pyramid.renderers import JSON

from cubicweb_api.util import get_api_path_prefix


def datetime_adapter(obj: Union[datetime, date, time], request):
    """
    Converts datetime, date and time object to an ISO string for JSON serialization
    :param obj: the object to convert
    :param request: the current request
    :return:
    """
    return obj.isoformat()


def includeme(config: Configurator):
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)
    json_renderer.add_adapter(date, datetime_adapter)
    json_renderer.add_adapter(time, datetime_adapter)

    config.add_renderer("cubicweb_api_json", json_renderer)
    config.include(".routes", route_prefix=get_api_path_prefix(config))
