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

import logging
import json

from flask import abort, request, jsonify, current_app
from cmdb.utils.wraps import json_required
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required
from cmdb.framework.cmdb_errors import TypeNotFoundError, TypeInsertError, ObjectDeleteError
from cmdb.framework.cmdb_type import CmdbType

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
type_blueprint = RootBlueprint('type_blueprint', __name__, url_prefix='/type')


@type_blueprint.route('/', methods=['GET'])
@login_required
def get_type_list():
    try:
        type_list = object_manager.get_all_types()
    except CMDBError:
        return abort(500)
    resp = make_response(type_list)
    return resp


@type_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
def get_type(public_id: int):
    try:
        type_instance = object_manager.get_type(public_id)
    except TypeNotFoundError:
        return abort(404)
    except CMDBError:
        return abort(500)
    resp = make_response(type_instance)
    return resp


@type_blueprint.route('/', methods=['POST'])
@login_required
def add_type():
    from bson import json_util
    from datetime import datetime
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_type_data['public_id'] = object_manager.get_new_id(CmdbType.COLLECTION)
        new_type_data['creation_time'] = datetime.utcnow()
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        type_instance = CmdbType(**new_type_data)
    except CMDBError as e:
        LOGGER.debug(e)
        return abort(400)
    try:
        ack = object_manager.insert_type(type_instance)
    except TypeInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@type_blueprint.route('/', methods=['PUT'])
@login_required
@json_required
def update_type():
    """TODO: Generate update log"""
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as e:
        LOGGER.warning(e)
        abort(400)
    try:
        update_type_instance = CmdbType(**new_type_data)
    except CMDBError:
        return abort(400)
    except CMDBError:
        return abort(500)

    try:
        object_manager.update_type(update_type_instance)
    except CMDBError:
        return abort(500)

    resp = make_response(update_type_instance)
    return resp


@type_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
def delete_type(public_id: int):
    try:
        # delete all objects by typeID
        object_manager.delete_many_objects({'type_id': public_id})
        ack = object_manager.delete_type(public_id=public_id)

    except TypeNotFoundError:
        return abort(400)
    except CMDBError:
        return abort(500)
    resp = make_response(ack)
    return resp


@type_blueprint.route('/delete/<string:public_ids>', methods=['GET'])
@login_required
def delete_many_types(public_ids):
    try:
        ids = []
        operator_in = {'$in': []}
        filter_public_ids = {'public_id': {}}

        for v in public_ids.split(","):
            try:
                ids.append(int(v))
            except (ValueError, TypeError):
                return abort(400)

        operator_in.update({'$in': ids})
        filter_public_ids.update({'public_id': operator_in})

        ack = object_manager.delete_many_types(filter_public_ids)
        return make_response(ack.raw_result)
    except TypeNotFoundError as e:
        return jsonify(message='Delete Error', error=e.message)
    except ObjectDeleteError as e:
        return jsonify(message='Delete Error', error=e.message)
    except CMDBError:
        return abort(500)


@type_blueprint.route('/count/', methods=['GET'])
@login_required
def count_objects():
    try:
        count = object_manager.count_types()
        resp = make_response(count)
    except CMDBError:
        return abort(400)
    return resp


@type_blueprint.route('/category/<int:public_id>', methods=['GET'])
@login_required
def get_type_by_category(public_id):
    try:
        type_list = object_manager.get_types_by(**{'category_id': public_id})
    except CMDBError:
        return abort(500)
    resp = make_response(type_list)
    return resp


@type_blueprint.route('/category/<int:public_id>', methods=['PUT'])
@login_required
def update_type_by_category(public_id):
    try:
        ack = object_manager.update_many_types(filter={'category_id': public_id}, update={'$set': {'category_id': 0}})
    except CMDBError:
        return abort(500)
    return make_response(ack.raw_result)
