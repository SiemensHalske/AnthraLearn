from functools import wraps
from flask import redirect, url_for
from flask_jwt_extended import verify_jwt_in_request


def jwt_required_optional(fallback_endpoint='auth.login'):
    """Ein Dekorator, der prüft, ob ein gültiges JWT-Cookie vorhanden ist.
    Leitet zu einer alternativen Seite um, wenn das Cookie fehlt."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request(locations=['cookies'])
                return f(*args, **kwargs)
            except Exception as e:
                print(f'JWT not found or invalid: {e}')
                return redirect(url_for(fallback_endpoint))

        return decorated_function

    return decorator
