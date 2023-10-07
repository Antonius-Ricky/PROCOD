from flask import redirect, url_for, session
from functools import wraps

def protected_route(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper