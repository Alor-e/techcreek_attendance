# Generated by Django 2.2.1 on 2019-07-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0024_auto_20190703_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='test_score',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='program_specific',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Course'),
        ),
    ]