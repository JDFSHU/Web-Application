# Generated by Django 4.1.7 on 2023-02-21 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_sale_email_alter_sale_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='user',
        ),
    ]
