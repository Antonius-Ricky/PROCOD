from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

#decorator for protected route
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper