# Generated by Django 4.1.4 on 2022-12-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_cart_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='users',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]