# Generated by Django 2.2 on 2021-02-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magic_link', '0002_auto_20210218_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='magiclinkhash',
            name='user_id',
            field=models.IntegerField(default=False),
        ),
    ]
