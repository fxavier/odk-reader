# Generated by Django 4.2.6 on 2023-10-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estruturashabitacionais',
            name='a_igreja_e',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='estruturashabitacionais',
            name='a_obra_e',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
