# Generated by Django 3.2 on 2022-05-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryapp', '0002_alter_diary_advice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='emoji',
            field=models.ImageField(blank=True, null=True, upload_to='emoji/'),
        ),
    ]
