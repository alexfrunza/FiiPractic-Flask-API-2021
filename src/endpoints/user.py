from flask import Blueprint, Response, request

from src.models.user import User
import json

from src.utils.decorators import session, http_handling

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('', methods=['GET'])
@http_handling
@session
def get_users(context):
    users = User.get_users(context)
    return Response(status=200, response=json.dumps(users))


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
def put_user(user_id, context):
    body = request.json
    User.update_user(context, body, user_id)
    return Response(status=200, response="Resource updated")


@user_bp.route('/<int:user_id>', methods=['PATCH'])
@http_handling
@session
def patch_user(context, user_id):
    body = request.json
    User.partial_update_user(context, body, user_id)
    return Response(status=200, response="Resource updated")


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@http_handling
@session
def delete_user(user_id, context):
    User.deactivate(context, user_id)
    return Response(status=200, response="Resource deleted")
