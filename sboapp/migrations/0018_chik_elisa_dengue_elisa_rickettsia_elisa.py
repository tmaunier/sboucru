# Generated by Django 2.0.3 on 2018-06-05 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sboapp', '0017_auto_20180605_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chik_elisa',
            fields=[
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='sboapp.Elisa')),
                ('sample_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('negative_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('cut_off_1_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('cut_off_2_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('positive_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('cut_off', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('novatech_units', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('result_chik', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'Chik_elisa',
            },
        ),
        migrations.CreateModel(
            name='Dengue_elisa',
            fields=[
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='sboapp.Elisa')),
                ('sample_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('negative_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('positive_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('calibrator_1_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('calibrator_2_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('calibrator_3_absorbance', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('cal_factor', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('cut_off', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('positive_cut_off_ratio', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('dengue_index', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('panbio_unit', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('result_dengue', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'Dengue_elisa',
            },
        ),
        migrations.CreateModel(
            name='Rickettsia_elisa',
            fields=[
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='sboapp.Elisa')),
                ('scrub_typhus', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('typhus', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
            ],
            options={
                'db_table': 'Rickettsia_elisa',
            },
        ),
    ]
