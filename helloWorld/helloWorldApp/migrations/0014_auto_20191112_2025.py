# Generated by Django 2.2.5 on 2019-11-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloWorldApp', '0013_auto_20191112_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='image',
            field=models.ImageField(blank=True, max_length=144, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='image_description',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]