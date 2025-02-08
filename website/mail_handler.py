from website import mail
from flask_mail import Message
from flask import render_template, url_for, flash
from socket import gaierror


def mail_sender(mail_identifier, target, data=None) -> None:
    try:    
        if mail_identifier == "reset_password":
            msg = Message("Změna hesla na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
            mail.send(msg)
        elif mail_identifier == "confirm_email":
            msg = Message("Potvrzení e-mailu na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/cz_confirm_email.html", url=url_for("auth_views.confirm_email", token = data, _external = True))
            mail.send(msg)
        elif mail_identifier == "nove_dite":
            msg = Message("Nové dítě na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/nove_dite.html")
    except gaierror:
        flash(f"Gaierror, pravděpodobně nejsi online. E-mail se neposlal. Mail identifier: {mail_identifier}, target: {target}", category="info")
