# Generated by Django 2.1.5 on 2020-06-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='label',
            field=models.CharField(max_length=500),
        ),
    ]
