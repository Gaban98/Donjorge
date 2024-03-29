# Generated by Django 4.2.3 on 2023-09-16 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_remove_cars_date_purchase_alter_cars_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="state",
            field=models.CharField(
                choices=[
                    ("Activo", "Activo"),
                    ("Comprado", "Comprado"),
                    ("Anulado", "Anulado"),
                ],
                default="activo",
                max_length=100,
            ),
        ),
    ]
