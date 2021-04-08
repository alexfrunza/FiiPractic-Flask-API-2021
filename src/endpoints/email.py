from flask import request, Blueprint, Response

from src.models.user import User
from src.utils.decorators import http_handling, session, is_authorized

email_bp = Blueprint('email', __name__, url_prefix="")


@email_bp.route('/email-confirmation', methods=["GET"])
@http_handling
@session
def activate_user(context):
    token = request.args.get('token')
    User.activate_user(context, token)
    return Response(status=200, response="Account activated")


@email_bp.route('/resend-email-confirmation', methods=["PATCH"])
@http_handling
@session
@is_authorized
def resend_email_confirmation(context, user):
    User.resend_email_confirmation(context, user.id)
    return Response(status=200, response="Email confirmation sent")
