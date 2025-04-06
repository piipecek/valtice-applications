from website import mail
from flask_mail import Message
from flask import render_template, url_for, flash
from socket import gaierror
from smtplib import SMTPRecipientsRefused


def mail_sender(mail_identifier, target, data=None) -> None:
    try:    
        if mail_identifier == "reset_password":
            msg = Message("Změna hesla na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/cz_reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
        elif mail_identifier == "en_reset_password":
            msg = Message("Password reset on ISSEM",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/en_reset_password.html", url=url_for("auth_views.en_reset_password", token = data, _external = True))
        elif mail_identifier == "confirm_email":
            msg = Message("Potvrzení e-mailu na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/cz_confirm_email.html", url=url_for("auth_views.confirm_email", token = data, _external = True))
        elif mail_identifier == "en_confirm_email":
            msg = Message("E-mail confirmation on ISSEM",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/en_confirm_email.html", url=url_for("auth_views.en_confirm_email", token = data, _external = True))
        elif mail_identifier == "cz_new_child":
            msg = Message("Nové dítě na Valtickém přihláškovém systému",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/cz_new_child.html")
        elif mail_identifier == "en_new_child":
            msg = Message("New child on ISSEM",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/en_new_child.html")
        elif mail_identifier == "send_calculation":
            msg = Message("Platba za MLŠSH",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/cz_calculation.html", data=data)
        elif mail_identifier == "en_send_calculation":
            msg = Message("ISSEM payment",
                        sender="application@early-music.cz",
                        recipients=[target])
            msg.html = render_template("mails/en_calculation.html", data=data)
        mail.send(msg)
    except gaierror:
        flash(f"Gaierror, pravděpodobně nejsi online. E-mail se neposlal. Mail identifier: {mail_identifier}, target: {target}", category="info")
    except SMTPRecipientsRefused:
        flash(f"SMTPRecipientsRefused, e-mail se nepodařilo odeslat. Kontaktujte organizátory.", category="info")
