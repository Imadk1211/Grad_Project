# Generated by Django 4.2.4 on 2024-04-15 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_secretary_secid_alter_staff_secid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='Name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
