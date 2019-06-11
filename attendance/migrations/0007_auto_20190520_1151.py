# Generated by Django 2.2.1 on 2019-05-20 10:51

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_auto_20190516_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='local_govt',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='state_of_origin', chained_model_field='state', null=True, on_delete=django.db.models.deletion.CASCADE, to='attendance.Local_govt', verbose_name='Local Government'),
        ),
    ]