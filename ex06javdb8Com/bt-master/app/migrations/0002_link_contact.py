# Generated by Django 2.1.1 on 2019-03-06 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
