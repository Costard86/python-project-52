# Generated by Django 5.0.1 on 2024-03-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, to='label.label', verbose_name='Labels'),
        ),
    ]
