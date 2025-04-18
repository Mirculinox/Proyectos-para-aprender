# Generated by Django 5.0.6 on 2024-05-13 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Articulos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=30)),
                ("seccion", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Clientes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=30)),
                ("direccion", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("tlfno", models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name="Pedidos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero", models.IntegerField()),
                ("fecha", models.DateField()),
                ("entregado", models.BooleanField()),
            ],
        ),
    ]
