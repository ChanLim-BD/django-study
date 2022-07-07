# Generated by Django 4.0.5 on 2022-07-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_gender_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='48px * 48px 크기의 png/jpg 파일을 업로드해주세요.', upload_to='avatar/profile/%Y/%m/%d'),
        ),
    ]