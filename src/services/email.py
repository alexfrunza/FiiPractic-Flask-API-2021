import logging
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

import settings
from src.enums.email import COMPANY_ADDED_TEMPLATE, EMAIL_CONFIRMATION_TEMPLATE

logger = logging.getLogger(__name__)


class EmailService:

    def __init__(self, api_key, sender):
        self.api_key = api_key
        self.sender = sender

        if not api_key:
            logger.error("Email service is not configured. SENDGRID_API_KEY is not set.")

        if not sender:
            logger.error("Email service is not configured. EMAIL_ADDRESS is not set.")

    def send_email(self, to, subject, content):
        mail = Mail(
            from_email=self.sender,
            to_emails=to,
            subject=subject,
            html_content=content
        )
        try:
            sgc = SendGridAPIClient(self.api_key)
            sgc.send(mail)
        except Exception as e:
            logger.error(f'We were unable to send an email to {to}')
            logger.error(e, exc_info=True)

    def send_assignment_email(self, user, company):
        email_content = COMPANY_ADDED_TEMPLATE.format(user.first_name, company.name)
        self.send_email(user.email, f"You have been assigned to {company.name}", email_content)

    def send_confirmation_email(self, user, token):
        url = f'http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/email-confirmation?token={token}'
        email_content = EMAIL_CONFIRMATION_TEMPLATE.format(user.first_name, url)
        self.send_email(user.email, "Welcome to FiiPractic", email_content)

