# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Routes for rendered objects.
"""

import logging

from werkzeug.exceptions import abort

from cmdb.framework.cmdb_object_manager import object_manager
from cmdb.framework.cmdb_errors import ObjectManagerGetError
from cmdb.framework.cmdb_render import CmdbRender, RenderError, RenderList
from cmdb.interface.route_utils import RootBlueprint, make_response, insert_request_user
from cmdb.user_management.user import User

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
render_routes = RootBlueprint('render_rest', __name__, url_prefix='/render')


@render_routes.route('/', methods=['GET'])
@insert_request_user
def get_rendered_object_list(request_user: User):
    """
    get all objects in database
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    try:
        object_list = object_manager.get_all_objects()
    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)
    if len(object_list) < 1:
        return make_response(object_list, 204)

    rendered_list = RenderList(object_list, request_user).render_result_list()

    return make_response(rendered_list)


@render_routes.route('/<int:public_id>/', methods=['GET'])
@render_routes.route('/<int:public_id>', methods=['GET'])
@insert_request_user
def get_rendered_object(public_id: int, request_user: User):
    """
    get specific object
    Args:
        public_id: Database ID of request object
        request_user: auto inserted user who made the request.
    Returns:
        requested object with given public id
    """
    try:
        object_instance = object_manager.get_object(public_id=public_id)
        type_instance = object_manager.get_type(public_id=object_instance.get_type_id())
    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)

    try:
        render = CmdbRender(object_instance=object_instance, type_instance=type_instance, render_user=request_user)
        render_result = render.result()
    except RenderError as err:
        LOGGER.error(err.message)
        return abort(500)

    return make_response(render_result)


@render_routes.route('/type/<int:type_id>', methods=['GET'])
@insert_request_user
def get_rendered_objects_by_type(type_id: int, request_user: User):
    """
    get all objects in database with given type id
    Args:
        type_id: type id of the object
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    try:
        object_list = object_manager.get_objects_by_type(type_id=type_id)

    except ObjectManagerGetError as err:
        LOGGER.error(err.message)
        return abort(404)
    try:
        rendered_list = RenderList(object_list, request_user).render_result_list()

    except RenderError as err:
        LOGGER.error(err.message)
        return abort(500)
    if len(rendered_list) < 1:
        return make_response(rendered_list, 204)
    resp = make_response(rendered_list)
    return resp


# SPECIAL ROUTES
@render_routes.route('/newest', methods=['GET'])
@render_routes.route('/newest/', methods=['GET'])
@insert_request_user
def get_newest(request_user: User):
    """
    get object with newest creation time
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    newest_objects_list = object_manager.get_objects_by(sort='creation_time',
                                                        limit=25,
                                                        active={"$eq": True},
                                                        creation_time={'$ne': None})
    rendered_list = RenderList(newest_objects_list, request_user).render_result_list()
    if len(rendered_list) < 1:
        return make_response(rendered_list, 204)
    return make_response(rendered_list)


@render_routes.route('/latest', methods=['GET'])
@render_routes.route('/latest/', methods=['GET'])
@insert_request_user
def get_latest(request_user: User):
    """
    get object with newest last edit time
    Args:
        request_user: auto inserted user who made the request.
    Returns:
        list of rendered objects
    """
    last_objects_list = object_manager.get_objects_by(sort='last_edit_time',
                                                      limit=25,
                                                      active={"$eq": True},
                                                      last_edit_time={'$ne': None})
    rendered_list = RenderList(last_objects_list, request_user).render_result_list()
    if len(rendered_list) < 1:
        return make_response(rendered_list, 204)
    return make_response(rendered_list)
