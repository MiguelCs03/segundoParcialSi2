# Generated by Django 5.1.8 on 2025-05-23 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materia", "0004_remove_detallemateria_usuario_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="detallemateria",
            name="profesor",
            field=models.ForeignKey(
                help_text="Profesor asignado a la materia",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detalles_materia",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
