# Generated by Django 3.2.9 on 2021-12-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hood_app', '0004_alter_hood_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hood',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
