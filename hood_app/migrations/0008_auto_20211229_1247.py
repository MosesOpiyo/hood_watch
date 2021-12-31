# Generated by Django 3.2.9 on 2021-12-29 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hood_app', '0007_auto_20211229_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurence',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='occurence',
            name='hood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_events', to='hood_app.hood'),
        ),
    ]