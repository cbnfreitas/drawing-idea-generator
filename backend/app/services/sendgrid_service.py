import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ..core import s


def send_email(to, subject, html=None):
    # Skip email during tests
    if not s.SEND_GRID_API_KEY:
        return

    message = Mail(
        from_email=s.EMAILS_FROM_EMAIL,
        to_emails=to,
        subject=subject,
        html_content=html)
    try:
        sg = SendGridAPIClient(s.SEND_GRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e)
