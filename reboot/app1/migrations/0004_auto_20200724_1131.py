# Generated by Django 2.1.5 on 2020-07-24 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20200724_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section_class',
            old_name='co_owner',
            new_name='teacher',
        ),
    ]