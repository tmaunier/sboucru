# Generated by Django 2.0.3 on 2018-07-30 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sboapp', '0031_auto_20180730_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='serum',
            name='import_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
