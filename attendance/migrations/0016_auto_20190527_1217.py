# Generated by Django 2.2.1 on 2019-05-27 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_auto_20190527_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='linked_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attendance', to='attendance.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('date', 'linked_student')},
        ),
    ]