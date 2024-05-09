from website import mail
from flask_mail import Message
from flask import render_template, url_for, flash
from socket import gaierror


def mail_sender(mail_identifier, target, data) -> None:
    try:    
        if mail_identifier == "reset_password":
            msg = Message("Změna hesla na 3D Portálu",
                        sender="josef.latj@gmail.com",
                        recipients=[target])
            msg.html = render_template("mails/reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
            mail.send(msg)

        if mail_identifier == "potvrzeni_emailu":
            msg = Message("Potvrzení e-mailu na Pípovo stránkách",
                        sender="josef.latj@gmail.com",
                        recipients=[target])
            msg.html = render_template("mails/potvrzeni_emailu.html", url=url_for("user_views.ucet_overeny", token = data, _external = True))
            mail.send(msg)
    except gaierror:
        flash(f"Gaierror, pravděpodobně nejsi online. E-mail se neposlal. Mail identifier: {mail_identifier}, target: {target}", category="info")
