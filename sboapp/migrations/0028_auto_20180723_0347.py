# Generated by Django 2.0.3 on 2018-07-23 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sboapp', '0027_auto_20180715_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rickettsia_elisa',
            name='scrub_typhus',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='rickettsia_elisa',
            name='typhus',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True),
        ),
    ]
