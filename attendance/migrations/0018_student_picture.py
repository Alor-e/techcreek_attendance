# Generated by Django 2.2.1 on 2019-06-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_auto_20190527_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
