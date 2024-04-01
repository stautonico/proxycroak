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

blueprint = Blueprint("pastebin", __name__, url_prefix="/pastebin")


@blueprint.route("/")
def index():
    meta = {"title": "Pastebin",
            "description": "Save and share decklists with your friends",
            "tags": ["pastebin"]}
    return render_template("pages/pastebin/pastebin_index.html", meta=meta)