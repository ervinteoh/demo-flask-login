"""This module define utilities for SMTP Mail service."""
import os
from dataclasses import dataclass
from threading import Thread
from typing import List, Union

from flask import current_app
from flask_mail import Message

from src.extensions import mail
from src.settings import BASE_DIR, get_config


@dataclass
class Attachment:
    """Email attachment.

    :param name: The attachment name.
    :type name: str
    :param filename: The attachment filename.
    :type filename: str
    :param filetype: The attachment filetype.
    :type filetype: str
    :param directory: The attachment directory.
    :type directory: str
    :param type: The attachment type, defaults to None
    :type type: str
    """

    name: str
    filename: str
    filetype: str
    directory: str
    type: str = None

    @property
    def file(self) -> bytes:
        """The attachment file.

        :return: The attachment file.
        :rtype: bytes
        """
        return open(self.filepath, "rb").read()

    @property
    def filepath(self) -> str:
        """The attachment filepath.

        This filepath should be relative to the static folder.

        :return: The attachment filepath.
        :rtype: str
        """
        static_dir = os.path.join(BASE_DIR, get_config().STATIC_FOLDER)
        directory = os.path.join(static_dir, self.directory)
        return os.path.join(directory, self.filename)

    @property
    def headers(self) -> dict:
        """The attachment header.

        :return: The attachment header.
        :rtype: dict
        """
        return [["Content-ID", f"<{self.name}>"]]

    def __iter__(self):
        yield ("filename", self.filename)
        yield ("content_type", self.filetype)
        yield ("data", self.file)
        yield ("disposition", self.type)
        yield ("headers", self.headers)


@dataclass
class AttachmentIcon(Attachment):
    """Email attachment icon.

    :param name: The attachment name.
    :type name: str
    :param filename: The attachment filename.
    :type filename: str
    """

    def __init__(self, name, filename):
        super().__init__(
            name=name,
            filename=filename,
            filetype="image/png",
            directory="img\\icon",
            type="inline",
        )


def send_mail(
    subject: str,
    sender: str,
    recipients: Union[str, list],
    text_body: str,
    html_body: str = None,
    attachments: List[Attachment] = None,
    **kwargs,
):
    """Send an email.

    :param subject: The subject of the email.
    :type subject: str
    :param sender: The sender email address.
    :type sender: str
    :param recipients: The recipient(s) email address.
    :type recipients: Union[str, list]
    :param text_body: The email text body.
    :type text_body: str
    :param html_body: The email html body, defaults to None
    :type html_body: str, optional
    :param attachments: _description_, defaults to []
    :type attachments: list, optional
    """
    # pylint: disable=protected-access, too-many-arguments

    def send(app, msg):
        with app.app_context():
            mail.send(msg)

    current_app.logger.info("Sending email to %s: %s", ",".join(recipients), subject)
    attachments = attachments or []
    msg = Message(subject, sender=sender, recipients=recipients, **kwargs)
    msg.body = text_body
    msg.html = html_body

    for attachment in attachments:
        msg.attach(**dict(attachment))
    Thread(target=send, args=(current_app._get_current_object(), msg)).start()
