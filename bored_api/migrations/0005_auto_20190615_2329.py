# Generated by Django 2.1.5 on 2019-06-15 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bored_api', '0004_activity_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='participants',
            field=models.IntegerField(default=0),
        ),
    ]
