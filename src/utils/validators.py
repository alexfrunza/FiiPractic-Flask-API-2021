import re
from src.utils.exceptions import InvalidBody

####################
# User validators #
####################


def validate_user_body(body):
    validate_email(body.get('email', ''))
    validate_password(body.get('password', ""))


def partial_validate_user_body(body):
    email = body.get('email', '')
    if email:
        validate_email(email)


def validate_password(password):
    if not password:
        raise InvalidBody("You must provide a password", status=400)


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    result = re.search(regex, email)
    if not result:
        raise InvalidBody("Email address is not valid", status=400)


######################
# Company validators #
######################


def validate_company_body(body):
    validate_name(body.get("name", ''))
    validate_country(body.get('country', ''))


def partial_validate_company_body(body):
    pass


def validate_name(name):
    if not name:
        raise InvalidBody("You must provide a name", status=400)


def validate_country(country):
    if not country:
        raise InvalidBody("You must provide a country", status=400)


def validate_company_assignment(body):
    try:
        _ = body['user_id']
    except KeyError:
        raise InvalidBody("You must provide an user", status=400)
