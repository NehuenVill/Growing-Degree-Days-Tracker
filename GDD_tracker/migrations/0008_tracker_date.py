# Generated by Django 3.1.2 on 2021-05-06 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDD_tracker', '0007_auto_20210506_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
