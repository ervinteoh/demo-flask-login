"""This module defines unit test cases for the mail utilities defined
defined in ``services`` package in :file:`mail.py` module.
"""
import pytest
from flask_mail import Message
from pytest_mock import MockerFixture as Mocker

from src.services.mail import send_mail


@pytest.mark.usefixtures("app")
def test_send_mail(mocker: Mocker):
    """Send mail."""
    mock_send = mocker.patch("src.extensions.mail.send")
    msg_content = {
        "subject": "Email Subject",
        "sender": "noreply@company.com",
        "recipients": "example@company.com",
        "body": "A generated content.",
    }
    message = Message(**msg_content)
    msg_content["text_body"] = msg_content.pop("body")
    mocker.patch.object(Message, "__new__", return_value=message)
    send_mail(**msg_content)
    mock_send.assert_called_once_with(message)
