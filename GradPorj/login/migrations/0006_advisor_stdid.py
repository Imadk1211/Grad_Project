# Generated by Django 4.2.4 on 2024-04-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_advisor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='stdid',
            field=models.CharField(default=None, max_length=7),
        ),
    ]
