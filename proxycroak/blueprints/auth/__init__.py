import datetime
import hashlib
import base64
import re
from secrets import token_urlsafe

from flask_login import current_user, login_user, logout_user
from profanity_check import predict_prob

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from sqlalchemy import or_
import bcrypt

from proxycroak.models import User
from proxycroak.database import db
from proxycroak.util.email import censor_email, send_activation_email, send_password_reset_email
from proxycroak.const import RESERVED_USERNAMES

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    meta = {"title": "Login",
            "description": "Login to proxycroak",
            "tags": ["login"]}

    if request.method == "GET":
        if not current_user.is_authenticated:
            return render_template("pages/login.html", meta=meta)
        else:
            return redirect(url_for("ui.index"))
    else:
        username_or_email = request.form.get("username")
        password = request.form.get("password")

        errors = []

        if not username_or_email:
            errors.append("'username' or 'email' is required")

        if not password:
            errors.append("'password' is required")

        if len(errors) > 0:
            return render_template("pages/login.html", meta=meta, errors=errors)

        user_obj = User.query.filter(
            or_(User.email == username_or_email, User.username == username_or_email)).first()

        if not user_obj:
            return render_template("pages/login.html", meta=meta, errors=["Invalid credentials"])

        sha256_hash = hashlib.sha256(password.encode()).digest()
        base64_password = base64.b64encode(sha256_hash)
        if not bcrypt.checkpw(base64_password, user_obj.password.encode()):
            return render_template("pages/login.html", meta=meta, errors=["Invalid credentials"])

        result = login_user(user_obj)

        if not result:
            return render_template("pages/login.html", meta=meta, errors=["Something went wrong when signing in"])

        flash("Login successful", "success")
        return redirect(url_for("ui.index"))


@blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for("ui.index"))


@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    signup_meta = {"title": "Signup",
                   "description": "Make an account",
                   "tags": ["signup"]}

    if request.method == "GET":
        return render_template("pages/signup.html", meta=signup)
    else:
        meta = {
            "title": "Activation Sent",
            "description": "Sent activation email to your email address",
            "tags": ["activate"]
        }

        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        errors = []

        if not email:
            errors.append("'email' field is required")

        if not username:
            errors.append("'username' field is required")

        if not password:
            errors.append("'password' field is required")

        if len(errors) > 0:
            return render_template("pages/signup.html", meta=signup_meta, errors=errors)

        # Check if the provided username is a reserved username
        if username.lower() in RESERVED_USERNAMES:
            return render_template("pages/signup.html", meta=signup_meta, errors=[
                f"Provided credentials already in use. Choose a different username or password"])

        # NOTE: This may be removed due to either removing too much stuff or not removing enough
        # Try to filter out any profane usernames
        profanity_probability = predict_prob([username.lower()])[0]
        # If we have > 75% prediction, its profanity, so fail
        if profanity_probability > 0.75:
            return render_template("pages/signup.html", meta=signup_meta, errors=[
                f"Provided credentials already in use. Choose a different username or password"])

        # activate the email (using an overcomplicated regular expression)
        regex = r'^([a-zA-Z0-9_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'

        if not re.fullmatch(regex, email):
            return render_template("pages/signup.html", meta=signup_meta,
                                   errors=[f"'{email}' is not a valid email address"])

        # Check if a user with the given email or username already exists
        user_obj = User.query.filter(
            or_(User.email == email, User.username == username)).first()

        if user_obj:
            return render_template("pages/signup.html", meta=signup_meta, errors=[
                f"Provided credentials already in use. Choose a different username or password"])

        # Hash the user's password
        sha256_hash = hashlib.sha256(password.encode()).digest()
        base64_password = base64.b64encode(sha256_hash)
        hashed = bcrypt.hashpw(base64_password, bcrypt.gensalt()).decode()

        newuser = User(
            username=username,
            password=hashed,
            email=email
        )
        db.session.add(newuser)
        db.session.commit()

        # Generate the email activation token
        token = token_urlsafe(32)
        newuser.account_activation_token = token
        newuser.account_activation_expires = datetime.datetime.now() + datetime.timedelta(minutes=15)

        db.session.add(newuser)
        db.session.commit()

        # Send the activation email
        send_result = send_activation_email(email, token)

        if not send_result:
            return render_template("pages/signup.html", meta=signup_meta,
                                   errors=["Something went wrong when sending activation email"])

        return render_template("pages/activation_sent.html", meta=meta)


@blueprint.route("/activate", methods=["GET"])
def activate():
    meta = {
        "title": "Activate Account",
        "description": "Activate your account",
        "tags": ["activate"]
    }
    token = request.args.get("t")

    if not token:
        return abort(400)

    user_obj = User.query.filter_by(account_activation_token=token).first()

    if not user_obj:
        return abort(400)

    # If, for whatever reason, we're activated, but we still have a token, just delete the token
    if user_obj.account_activated:
        user_obj.account_activation_token = None
        user_obj.account_activation_expires = None
        db.session.add(user_obj)
        db.session.commit()

        return render_template("pages/account_activated.html", meta=meta)

    # Make sure the token is still valid
    if datetime.datetime.now() > user_obj.account_activation_expires:
        return render_template("pages/resend_activation.html", meta=meta, token=token,
                               censored_email=censor_email(user_obj.email))

    user_obj.account_activated = True
    user_obj.account_activated_at = datetime.datetime.now()
    user_obj.account_activation_token = None
    user_obj.account_activation_expires = None
    user_obj.updated_at = datetime.datetime.now()

    db.session.add(user_obj)
    db.session.commit()

    return render_template("pages/account_activated.html", meta=meta)


@blueprint.route("/resend_activation", methods=["POST"])
def resend_activation():
    meta = {
        "title": "Activation Sent",
        "description": "Sent activation email to your email address",
        "tags": ["activate"]
    }

    email = request.form.get("email")
    token = request.form.get("token")

    if not email or not token:
        return abort(400)

    # Grab the user by their email and make sure the token matches
    user_obj = User.query.filter_by(email=email).first()

    if not user_obj:
        # TODO: Return to the resend activation page
        abort(400)

    # To prevent spamming, only resend the email if the token in the db is expired
    if datetime.datetime.now() < user_obj.account_activation_expires:
        # TODO: Send something better
        return "<h1>Email already sent</h1>"

    if user_obj.account_activation_token != token:
        return abort(400)

    # Generate the email activation token
    token = token_urlsafe(32)
    user_obj.account_activation_token = token
    user_obj.account_activation_expires = datetime.datetime.now() + datetime.timedelta(minutes=15)

    send_activation_email(email, token)

    db.session.add(user_obj)
    db.session.commit()

    return render_template("pages/activation_sent.html", meta=meta)


@blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    meta = {
        "title": "Forgor Password?",
        "description": "Did you forgor you password? Here's where you reset it",
        "tags": ["forgot"]
    }

    if request.method == "GET":
        return render_template("pages/forgot_password.html", meta=meta)
    else:
        email = request.form.get("email")

        if not email:
            return render_template("pages/forgot_password.html", meta=meta, errors=["An email is required"])

        user_obj = User.query.filter_by(email=email).first()

        if user_obj:
            # Don't send a password reset if we have one and it's still valid
            if user_obj.password_reset_token is None or user_obj.password_reset_expires < datetime.datetime.now():
                # Generate the email activation token
                token = token_urlsafe(32)
                user_obj.password_reset_token = token
                user_obj.password_reset_expires = datetime.datetime.now() + datetime.timedelta(minutes=15)
                db.session.add(user_obj)
                db.session.commit()
                send_password_reset_email(email, token)

        return render_template("pages/password_reset_sent.html", meta=meta)


@blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    meta = {
        "title": "Reset Password",
        "description": "Reset your password",
        "tags": ["resetpassword"]
    }

    if request.method == "GET":
        token = request.args.get("t")

        if not token:
            return abort(400)

        user_obj = User.query.filter_by(password_reset_token=token).first()

        if not user_obj:
            return abort(500)

        # Make sure the token is still valid
        if datetime.datetime.now() > user_obj.password_reset_expires:
            user_obj.password_reset_token = None
            user_obj.password_reset_expires = None
            db.session.commit()

            return render_template("pages/forgot_password.html", meta=meta, errors=[
                "This password reset link is expired, please enter your email to send a new password reset link."])

        return render_template("pages/password_reset.html", meta=meta, token=token)

    else:
        token = request.form.get("token")
        password = request.form.get("password")

        if not token:
            return abort(500)

        if not password:
            return render_template("pages/password_reset.html", meta=meta, token=token,
                                   errors=["A password is required"])

        user_obj = User.query.filter_by(password_reset_token=token).first()

        if not user_obj:
            return abort(500)

        # Make sure the token is still valid
        if datetime.datetime.now() > user_obj.password_reset_expires:
            return render_template("pages/password_reset_expired.html", meta=meta)

        sha256_hash = hashlib.sha256(password.encode()).digest()
        base64_password = base64.b64encode(sha256_hash)
        hashed = bcrypt.hashpw(base64_password, bcrypt.gensalt()).decode()

        user_obj.password = hashed

        user_obj.password_reset_token = None
        user_obj.password_reset_expires = None

        user_obj.updated_at = datetime.datetime.now()

        db.session.add(user_obj)
        db.session.commit()

        return render_template("pages/password_reset_success.html", meta=meta)
