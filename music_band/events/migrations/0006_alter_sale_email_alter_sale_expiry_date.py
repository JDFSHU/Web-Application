# Generated by Django 4.1.7 on 2023-02-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_sale_email_alter_sale_card_number_alter_sale_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='email',
            field=models.EmailField(default='c1004433@exchange.shu.ac.uk', max_length=254),
        ),
        migrations.AlterField(
            model_name='sale',
            name='expiry_date',
            field=models.CharField(default='12/12', max_length=5),
        ),
    ]