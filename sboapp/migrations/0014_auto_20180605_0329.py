# Generated by Django 2.0.3 on 2018-06-05 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sboapp', '0013_auto_20180605_0317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chik_elisa',
            old_name='result_id',
            new_name='result',
        ),
        migrations.RenameField(
            model_name='dengue_elisa',
            old_name='result_id',
            new_name='result',
        ),
        migrations.RenameField(
            model_name='elisa',
            old_name='sample_id',
            new_name='sample',
        ),
        migrations.RenameField(
            model_name='rickettsia_elisa',
            old_name='result_id',
            new_name='result',
        ),
    ]
