import functools
import logging
import json
from flask import Response
from database_management import get_database_session

logger = logging.getLogger(__name__)


def session(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        context = get_database_session()
        kwargs['context'] = context

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            context.close()

    return wrapper


def http_handling(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            status = getattr(e, 'status', 500)
            return Response(status=status, response=json.dumps({'error': e.args[0]}))

    return wrapper
