# Generated by Django 2.0.3 on 2018-05-15 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sboapp', '0004_auto_20180508_0512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chik_elisa',
            name='result_id',
        ),
        migrations.RemoveField(
            model_name='dengue_elisa',
            name='result_id',
        ),
        migrations.RemoveField(
            model_name='elisa',
            name='sample_id',
        ),
        migrations.RemoveField(
            model_name='pma',
            name='sample_id',
        ),
        migrations.RemoveField(
            model_name='pma_result',
            name='ag_array_id',
        ),
        migrations.RemoveField(
            model_name='rickettsia_elisa',
            name='result_id',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='site_id',
            new_name='site',
        ),
        migrations.AlterField(
            model_name='freezer',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='sboapp.Serum'),
        ),
        migrations.AlterField(
            model_name='serum',
            name='site',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sboapp.Site'),
        ),
        migrations.AlterField(
            model_name='serum',
            name='ward',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sboapp.Ward'),
        ),
        migrations.DeleteModel(
            name='Chik_elisa',
        ),
        migrations.DeleteModel(
            name='Dengue_elisa',
        ),
        migrations.DeleteModel(
            name='Elisa',
        ),
        migrations.DeleteModel(
            name='Pma',
        ),
        migrations.DeleteModel(
            name='Pma_result',
        ),
        migrations.DeleteModel(
            name='Rickettsia_elisa',
        ),
    ]
