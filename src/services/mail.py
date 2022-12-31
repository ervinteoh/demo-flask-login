"""This module define utilities for SMTP Mail service."""
from threading import Thread

from flask import current_app
from flask_mail import Message

from src.extensions import mail


def send_mail(subject, sender, recipients, text_body, html_body=None, **kwargs):
    """Send an email.

    :param subject: The subject of the email.
    :type subject: str
    :param sender: The sender email address.
    :type sender: str
    :param recipients: The recipient(s) email address.
    :type recipients: (str, list)
    :param text_body: The contents of the email body as text.
    :type text_body: str
    :param html_body: The contents of the email body as html, defaults to None
    :type html_body: str, optional
    """
    # pylint: disable=protected-access

    def send(app, msg):
        with app.app_context():
            mail.send(msg)

    current_app.logger.info("Sending email to %s: %s", ",".join(recipients), subject)
    msg = Message(subject, sender=sender, recipients=recipients, **kwargs)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send, args=(current_app._get_current_object(), msg)).start()
