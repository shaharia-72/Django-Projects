# Generated by Django 5.1.1 on 2024-09-16 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0005_alter_event_event_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(default='GALL-292121', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_image',
            field=models.ImageField(blank=True, null=True, upload_to='events_images/'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='transition_id',
            field=models.CharField(default='WPKL-829609', max_length=10),
        ),
    ]
