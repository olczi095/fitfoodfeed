import secrets
from datetime import timedelta
from typing import Any

from django.core.mail import EmailMessage
from django.utils import timezone
from PIL import Image

from fitfoodfeed.settings import EMAIL_HOST_USER


def prepare_mail_message(product_name: str, product_brand: str,
                         product_category: str, product_description: str,
                         user_email: str) -> str:
    """
    Prepare the message content for the proposed product review email, sending by user.
    """
    message = (
        f"Name: {product_name}\n"
        f"Brand: {product_brand}\n"
        f"Category: {product_category}\n"
        f"Description: {product_description}\n\n"
        f"From user with e-mail: {user_email}"
    )
    return message

def generate_mail_data(product_name: str, message: str,
                       user_email: str, product_image: Image) -> dict:
    """
    Generate the mail data for the proposed product review email, sending by user.
    """
    subject = f"New proposed product for review: {product_name}"
    mail_data = {
        'subject': subject, 
        'message': message,
        'user_email': user_email, 
        'image': product_image
    }
    return mail_data

def send_email_with_product_for_review(mail_data: dict[str, Any]) -> None:
    subject = mail_data['subject']
    message = mail_data['message']
    user_email = mail_data['user_email']
    product_image = mail_data.get('product_image', None)

    email = EmailMessage(
        subject,
        message,
        user_email,
        [EMAIL_HOST_USER],
    )

    if product_image:
        email.attach(product_image.name, product_image.read(), product_image.content_type)

    email.send(fail_silently=False)

def generate_confirmation_data() -> str:
    """
    Generate confirmation data:
    a random confirmation code and confirmation date for e-mail verification.
    """
    confirmation_code = secrets.token_urlsafe(16)
    confirmation_date = timezone.now() + timedelta(hours=24)
    confirmation_data = {
        'confirmation_code': confirmation_code,
        'confirmation_date': confirmation_date.isoformat()
    }
    return confirmation_data
