# Generated by Django 2.2 on 2021-02-18 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magic_link', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magiclinkhash',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
