"""Initialise the Flask meme app.

For exception coding see:
https://werkzeug.palletsprojects.com/en/2.1.x/exceptions/
"""

##############################
# Imports
##############################
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
from cryptography.fernet import Fernet


##############################
# Coding
##############################

def page_not_found(NotFound):
    """Take care if page is not found. Send message to user."""
    return render_template('404.html'), 404


def internal_server_error(InternalServerError):
    """Take care if server error appears. Send message to user."""
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


def get_app_instance():
    """
    Return the app instance using customised error handlers.

    Set some security configurations according this blog post:
    https://www.securecoding.com/blog/flask-security-best-practices/
    and
    https://testdriven.io/blog/csrf-flask/

    Security test happens via Snyk app on https://app.snyk.io
    """
    key = Fernet.generate_key()
	
    app = Flask(__name__,
                template_folder='../templates', static_folder='../static')

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
		SESSION_COOKIE_SAMESITE='Lax',
        SECRET_KEY=key,
    )
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    csrf = CSRFProtect()
    csrf.init_app(app)

    return app
