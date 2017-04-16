# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-15 22:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_from_twitter', models.CharField(max_length=200)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TweetClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, unique=True)),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TweetDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TweetTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manual_tagging.TweetClassification')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manual_tagging.Tweet')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manual_tagging.TweetDataset'),
        ),
        migrations.AddField(
            model_name='tweet',
            name='previous_classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manual_tagging.TweetClassification'),
        ),
    ]