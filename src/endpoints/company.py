from flask import Blueprint, Response, request
from src.utils.decorators import http_handling, session, is_authorized, is_admin, action_log
from src.models.company import Company
from src.models.user_company import UserCompany
import json

company_bp = Blueprint('companies', __name__, url_prefix='/companies')


@company_bp.route('', methods=['GET'])
@http_handling
@session
@is_authorized
@is_admin
def get_companies(context, user):
    companies = Company.get_companies(context)
    return Response(status=200, response=json.dumps(companies))


@company_bp.route('', methods=['POST'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="CREATE COMPANY")
def post_company(context, user):
    body = request.json
    Company.create_company(context, body)
    return Response(status=201, response="Resource created")


@company_bp.route('/<int:company_id>', methods=['PUT'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="UPDATE COMPANY")
def put_company(context, company_id, user):
    body = request.json
    Company.update_company(context, body, company_id)
    return Response(status=200, response="Resource updated")


@company_bp.route('/<int:company_id>', methods=["PATCH"])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="UPDATE COMPANY")
def patch_company(context, company_id, user):
    body = request.json
    Company.partial_update_company(context, body, company_id)
    return Response(status=200, response="Resource updated")


@company_bp.route('/<int:company_id>', methods=['DELETE'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="DELETE COMPANY")
def delete_company(context, company_id, user):
    Company.delete_company(context, company_id)
    return Response(status=200, response="Resource deleted")


@company_bp.route('/<int:company_id>/assign/', methods=["PATCH"])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="USER ASSIGNED TO COMPANY")
def company_assign(context, company_id, user):
    UserCompany().assign_to_company(context, company_id, request.json)
    return Response(status=200, response="User assigned to company")


@company_bp.route('/<int:company_id>/users', methods=["GET"])
@http_handling
@session
@is_authorized
@is_admin
def get_company_users(context, company_id, user):
    users = UserCompany.get_company_users(context, company_id)
    return Response(status=200, response=json.dumps(users))

