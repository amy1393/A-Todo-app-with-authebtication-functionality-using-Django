# Generated by Django 3.0.5 on 2020-04-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date_on_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
