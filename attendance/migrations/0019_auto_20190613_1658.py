# Generated by Django 2.2.1 on 2019-06-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0018_student_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='local_govt',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Local Government'),
        ),
    ]