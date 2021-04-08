from flask import Blueprint, Response, request

from src.models.user import User
import json

from src.utils.decorators import session, http_handling, is_authorized, is_admin_or_self, is_admin, action_log, \
    is_active

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('', methods=['GET'])
@http_handling
@session
@is_authorized
@is_active
def get_users(context, user):
    users = User.get_users(context, request)
    return Response(status=200, response=json.dumps(users), content_type='application/json')


@user_bp.route('', methods=['POST'])
@http_handling
@session
def post_user(context):
    body = request.json
    User.create_user(context, body)
    return Response(status=201, response="Resource created")


@user_bp.route('/<int:user_id>', methods=['PUT'])
@http_handling
@session
@is_authorized
@is_admin_or_self
@is_active
@action_log(action="UPDATE USER")
def put_user(user_id, context, user):
    body = request.json
    User.update_user(context, body, user_id)
    return Response(status=200, response="Resource updated")


@user_bp.route('/<int:user_id>', methods=['PATCH'])
@http_handling
@session
@is_authorized
@is_admin_or_self
@is_active
@action_log(action="UPDATE USER")
def patch_user(context, user_id, user):
    body = request.json
    User.partial_update_user(context, body, user_id)
    return Response(status=200, response="Resource updated")


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@http_handling
@session
@is_authorized
@is_admin
@is_active
@action_log(action="DELETE USER")
def delete_user(user_id, context, user):
    User.deactivate(context, user_id)
    return Response(status=200, response="Resource deleted")
