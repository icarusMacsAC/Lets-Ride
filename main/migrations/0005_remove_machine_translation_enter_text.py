# Generated by Django 4.0.4 on 2022-11-08 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_machine_translation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine_translation',
            name='enter_text',
        ),
    ]
