# Generated by Django 4.1.6 on 2023-02-13 23:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birthdate",
            field=models.DateField(null=True),
        ),
    ]
