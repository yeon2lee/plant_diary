# Generated by Django 3.2.6 on 2021-08-30 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
