# Generated by Django 4.2.13 on 2024-07-10 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendorhandles",
            name="tool",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app1.instrumentmodel"
            ),
        ),
    ]
