# Generated by Django 2.2.5 on 2019-11-26 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('helloWorldApp', '0015_auto_20191112_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='downvote',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('topics', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('num_members', models.IntegerField(null=True)),
                ('birthday', models.DateTimeField(auto_now_add=True, null=True)),
                ('image', models.ImageField(max_length=144, null=True, upload_to='subreddit/pic')),
                ('image_description', models.CharField(max_length=240, null=True)),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
