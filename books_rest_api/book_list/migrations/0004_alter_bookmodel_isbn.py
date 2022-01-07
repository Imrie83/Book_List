# Generated by Django 4.0.1 on 2022-01-06 16:37

import book_list.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_list', '0003_alter_bookmodel_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='isbn',
            field=models.CharField(max_length=255, validators=[book_list.models.validate_isbn], verbose_name='ISBN'),
        ),
    ]