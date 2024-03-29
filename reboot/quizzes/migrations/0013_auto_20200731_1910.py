# Generated by Django 2.1.5 on 2020-07-31 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0012_auto_20200731_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz_point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='pointer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='quiz_point',
            name='quiz_fro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='quizzes.Quiz'),
        ),
        migrations.AddField(
            model_name='quiz_point',
            name='quiz_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='quizzes.Quiz'),
        ),
    ]
