# Generated by Django 5.0.10 on 2025-04-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_donhang_ghichu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donhang',
            name='ghichu',
            field=models.TextField(),
        ),
    ]
