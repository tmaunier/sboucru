# Generated by Django 2.0.3 on 2018-06-06 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sboapp', '0018_chik_elisa_dengue_elisa_rickettsia_elisa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chik_elisa',
            name='result',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sboapp.Elisa'),
        ),
        migrations.AlterField(
            model_name='dengue_elisa',
            name='result',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sboapp.Elisa'),
        ),
        migrations.AlterField(
            model_name='elisa',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sboapp.Serum'),
        ),
        migrations.AlterField(
            model_name='freezer',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sboapp.Serum'),
        ),
        migrations.AlterField(
            model_name='rickettsia_elisa',
            name='result',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sboapp.Elisa'),
        ),
    ]
