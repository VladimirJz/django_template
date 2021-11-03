# Generated by Django 3.2.6 on 2021-11-03 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0004_backups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backups',
            name='Location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backup_location', to='backups.locations'),
        ),
    ]
