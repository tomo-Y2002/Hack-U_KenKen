# Generated by Django 4.2.5 on 2023-09-09 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hoyou", "0018_alter_record_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="family_name",
            field=models.CharField(default="NO_NAME", max_length=100),
        ),
    ]
