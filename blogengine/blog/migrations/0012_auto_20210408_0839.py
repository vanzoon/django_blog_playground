# Generated by Django 3.1.4 on 2021-04-08 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True, db_index=True, verbose_name='Contents'),
        ),
    ]
