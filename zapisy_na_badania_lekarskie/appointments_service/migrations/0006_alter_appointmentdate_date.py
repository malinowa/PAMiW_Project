# Generated by Django 3.2.8 on 2021-12-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments_service', '0005_auto_20211218_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentdate',
            name='date',
            field=models.DateTimeField(blank=True, default=None, null=True, unique=True),
        ),
    ]
