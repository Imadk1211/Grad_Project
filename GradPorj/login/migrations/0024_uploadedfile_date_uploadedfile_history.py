# Generated by Django 4.2.4 on 2024-05-14 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0023_alter_uploadedfile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='Date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='history',
            field=models.CharField(default=None, max_length=50000),
        ),
    ]
