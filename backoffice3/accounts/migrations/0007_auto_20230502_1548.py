# Generated by Django 3.2.18 on 2023-05-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230502_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_rejected',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='reject_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
