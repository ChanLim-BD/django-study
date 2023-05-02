# Generated by Django 3.2.18 on 2023-05-02 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_recent_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_rejected',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
