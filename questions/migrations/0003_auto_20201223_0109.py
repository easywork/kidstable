# Generated by Django 2.1 on 2020-12-23 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20201221_0001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questiondao',
            old_name='questionText',
            new_name='question',
        ),
    ]
