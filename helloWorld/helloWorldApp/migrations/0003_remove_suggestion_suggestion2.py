# Generated by Django 2.2.5 on 2019-10-06 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helloWorldApp', '0002_suggestion_suggestion2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestion',
            name='suggestion2',
        ),
    ]
