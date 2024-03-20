import requests

import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from flask import request

from proxycroak.config import CONFIG

sg = sendgrid.SendGridAPIClient(api_key=CONFIG.SENDGRID_API_KEY)


def send_email(from_email, from_name, to, subject, content, is_html=True):
    data = {
        "from": f"{from_name} <{from_email}>",
        "to": [to],
        "subject": subject,
    }

    if is_html:
        data["html"] = content
    else:
        data["text"] = content

    r = requests.post("https://api.mailgun.net/v3/mail.proxycroak.com/messages",
                      auth=("api", CONFIG.MAILGUN_API_KEY),
                      data=data
                      )

    # TODO: Catch and log/report errors

    return r.status_code == 200


def censor_email(email):
    if "@" in email:
        username, domain = email.split("@")
        visible_username_length = min(1, len(username))
        censored_username = username[:visible_username_length] + "*" * (len(username) - visible_username_length)
        censored_domain = "*" * (len(domain) - 4) + domain[-4:]
        return censored_username + "@" + censored_domain
    else:
        visible_length = min(1, len(email))
        return email[:visible_length] + "*" * (len(email) - visible_length)


def send_activation_email(to, token):
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Activation</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
          <td align="center" bgcolor="#ffffff" style="padding: 40px 0;">
            <img src=`{url_root}static/img/favicons/favicon-196x196.png` alt="Site Logo" width="150" style="display: block;">
            <h2 style="margin-top: 20px;">Welcome to Proxycroak!</h2>
            <p style="margin-top: 20px;">Thank you for creating an account. To activate your account, please click the button below:</p>
            <p style="margin-top: 20px;"><a href="{url_root}auth/activate?t={token}" style="background-color: #00acd1; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Activate Your Account</a></p>
            <p style="margin-top: 20px;">If the button above doesn't work, you can copy and paste the following link into your browser:</p>
            <p>{url_root}auth/activate?t={token}</p>
            <small><i>This link expires 15 minutes from the time it was sent</i></small>
          </td>
        </tr>
      </table>
    </body>
    </html>
            """.format(token=token, url_root=request.url_root)

    return send_email("account-activation@mail.proxycroak.com", "Proxycroak Account Activation", to,
                      "Activate your Proxycroak account", html)


def send_password_reset_email(to, token):
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Activation</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
          <td align="center" bgcolor="#ffffff" style="padding: 40px 0;">
            <img src=`{url_root}static/img/favicons/favicon-196x196.png` alt="Site Logo" width="150" style="display: block;">
            <h2 style="margin-top: 20px;">We heard you forgot your password</h2>
            <p style="margin-top: 20px;">Click the button below to reset your password:</p>
            <p style="margin-top: 20px;"><a href="{url_root}auth/reset_password?t={token}" style="background-color: #00acd1; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Your Password</a></p>
            <p style="margin-top: 20px;">If the button above doesn't work, you can copy and paste the following link into your browser:</p>
            <p>{url_root}auth/reset_password?t={token}</p>
            <small><i>This link expires 15 minutes from the time it was sent</i></small>
          </td>
        </tr>
      </table>
    </body>
    </html>
            """.format(token=token, url_root=request.url_root)

    return send_email("password-reset@mail.proxycroak.com", "Proxycroak Account Reset", to,
                      "Reset your Proxycroak password", html)
