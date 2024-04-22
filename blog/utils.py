from typing import Any

from django.core.mail import EmailMessage

from blog.forms import ProductSubmissionForm
from fitfoodfeed.settings import EMAIL_HOST_USER


def prepare_product_review_email(form: ProductSubmissionForm) -> dict[str, Any]:
    """
    Prepare an email message with details of a proposed product for review.
    Getting from user by submitting form.
    """
    product_name = form.cleaned_data['name']
    product_brand = form.cleaned_data['brand']
    product_category = form.cleaned_data.get('category', '')
    product_description = form.cleaned_data.get('description', '')
    user_email = form.cleaned_data['user_email']
    product_image = form.cleaned_data.get('image', None)

    subject = f"New proposed product for review: {product_name}"
    message = (
        f"Name: {product_name}\n"
        f"Brand: {product_brand}\n"
        f"Category: {product_category}\n"
        f"Description: {product_description}\n\n"
        f"From user with e-mail: {user_email}"
    )
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
