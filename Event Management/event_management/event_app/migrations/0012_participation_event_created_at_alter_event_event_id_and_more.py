# Generated by Django 5.1.1 on 2024-09-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0011_alter_event_event_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='event_created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(default='RDIP-921645', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='participation',
            name='transition_id',
            field=models.CharField(default='LRZV-873756', max_length=11),
        ),
    ]
