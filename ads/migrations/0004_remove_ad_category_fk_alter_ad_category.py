# Generated by Django 5.2.1 on 2025-05-19 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_category_ad_category_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='category_fk',
        ),
        migrations.AlterField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ads.category'),
        ),
    ]
