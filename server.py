"""
    The Python server entry point.
"""

from flask import Flask

import settings
from database_management import build_sqlite_connection_string, init_database_connection
from src.endpoints.email import email_bp
from src.endpoints.user import user_bp
from src.endpoints.company import company_bp
from src.endpoints.login import login_bp


def configure_app(application):
    database_file_path = 'db/fii_practic_database'
    connection_string = build_sqlite_connection_string(database_file_path)
    init_database_connection(connection_string)


app = Flask(__name__)
configure_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(company_bp)
app.register_blueprint(login_bp)
app.register_blueprint(email_bp)


@app.route('/status', methods=['GET'])
def get_status():
    return 'The server is up and running!'


def main():
    """
        Fii practic - Server main
    """
    debug = settings.ENVIRONMENT == 'DEV'
    app.run(debug=debug, host=settings.SERVER_HOST, port=settings.SERVER_PORT)


if __name__ == '__main__':
    main()
