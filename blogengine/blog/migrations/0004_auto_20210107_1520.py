# Generated by Django 3.1.4 on 2021-01-07 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201226_0955'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date_pub',
            new_name='pub_date',
        ),
    ]
