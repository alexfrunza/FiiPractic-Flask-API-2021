"""
    The Python server entry point.
"""

from flask import Flask

from database_management import build_sqlite_connection_string, init_database_connection
from src.endpoints.user import user_bp
from src.endpoints.company import company_bp


def configure_app(application):
    database_file_path = 'fii_practic_database'
    connection_string = build_sqlite_connection_string(database_file_path)
    init_database_connection(connection_string)


app = Flask(__name__)
configure_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(company_bp)


@app.route('/status', methods=['GET'])
def get_status():
    return 'The server is up and running!'


def main():
    """
        Fii practic - Server main
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()
