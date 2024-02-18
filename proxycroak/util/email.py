import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

from proxycroak.config import CONFIG

sg = sendgrid.SendGridAPIClient(api_key=CONFIG.SENDGRID_API_KEY)


def send_email(to, subject, content, is_html=True):
    from_email = Email("account-activation@mail.proxycroak.com")
    to_email = To(to)
    content = Content("text/html" if is_html else "text/plain", content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    # TODO: Catch and log/report errors

    return response.status_code == 202


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
    # TODO: Find a way to set the domain dynamically
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
            <img src=`https://proxycroak.com/static/img/favicons/favicon-196x196.png` alt="Site Logo" width="150" style="display: block;">
            <h2 style="margin-top: 20px;">Welcome to Proxycroak!</h2>
            <p style="margin-top: 20px;">Thank you for creating an account. To activate your account, please click the button below:</p>
            <p style="margin-top: 20px;"><a href="https://proxycroak.com/auth/activate?t={token}" style="background-color: #00acd1; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">activate Your Account</a></p>
            <p style="margin-top: 20px;">If the button above doesn't work, you can copy and paste the following link into your browser:</p>
            <p>https://proxycroak.com/auth/activate?t={token}</p>
            <small><i>This link expires 15 minutes from the time it was sent</i></small>
          </td>
        </tr>
      </table>
    </body>
    </html>
            """.format(token=token)

    return send_email(to, "Activate your Proxycroak account", html)
