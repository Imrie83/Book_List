# Generated by Django 4.0.1 on 2022-01-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='self_link',
            field=models.CharField(max_length=255, null=True, verbose_name='self link'),
        ),
    ]
