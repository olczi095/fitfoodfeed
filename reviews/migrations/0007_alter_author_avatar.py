# Generated by Django 4.2.3 on 2023-07-12 10:49

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_author_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default-avatar.png', upload_to='avatars/', validators=[reviews.validators.validate_avatar_type, reviews.validators.validate_avatar_dimensions, reviews.validators.validate_avatar_size]),
        ),
    ]