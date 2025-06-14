# Generated by Django 5.2.1 on 2025-06-09 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libreta', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='libreta',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libretas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='libreta',
            name='gestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libretas', to='libreta.gestion'),
        ),
    ]
