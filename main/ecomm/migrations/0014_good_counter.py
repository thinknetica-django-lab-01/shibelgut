# Generated by Django 3.1.5 on 2021-02-20 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0013_auto_20210216_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]
