# Generated by Django 2.2.1 on 2019-05-16 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20190516_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50),
        ),
    ]
