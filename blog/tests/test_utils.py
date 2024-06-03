from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from blog.utils import send_email_with_product_for_review


class SendEmailWithProductTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'Test Product for review',
            'brand': 'Test Brand',
            'user_email': 'test_user@mail.com',
        }
        self.expected_subject = f"New proposed product for review: {self.valid_data['name']}"
        self.expected_message = (
            f"Name: {self.valid_data['name']}\n"
            f"Brand: {self.valid_data['brand']}\n"
            f"Category: {None}\n"
            f"Description: \n\n"
            f"From user with e-mail: {self.valid_data['user_email']}"
        )

    def test_send_email_without_product_image(self):
        mail_data = {
            'subject': self.expected_subject,
            'message': self.expected_message,
            'user_email': self.valid_data['user_email'],
        }
        send_email_with_product_for_review(mail_data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 0)

    def test_send_email_with_product_image(self):
        product_image = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        mail_data = {
            'subject': self.expected_subject,
            'message': self.expected_message,
            'user_email': self.valid_data['user_email'],
            'product_image': product_image
        }
        send_email_with_product_for_review(mail_data)

        sent_mail = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(sent_mail.attachments), 1)
        self.assertEqual(sent_mail.attachments[0][0], "image.jpg")
        self.assertEqual(sent_mail.attachments[0][1], b"file_content")
        self.assertEqual(sent_mail.attachments[0][2], "image/jpeg")
