# Generated by Django 5.1.1 on 2024-09-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0023_alter_event_event_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(default='PIOP-106578', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='participation',
            name='transition_id',
            field=models.CharField(default='JCWH-728512', max_length=11, unique=True),
        ),
    ]
