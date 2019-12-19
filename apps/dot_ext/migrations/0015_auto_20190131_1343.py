# Generated by Django 2.1.2 on 2019-01-31 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dot_ext', '0014_auto_20190121_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='applicationlabel',
            name='applications',
            field=models.ManyToManyField(to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL),
        ),
    ]
