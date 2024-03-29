# Generated by Django 3.2.3 on 2023-06-14 21:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20230607_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^#(?:[0-9a-fA-F]{3}){1,2}$')], verbose_name='Цветовой HEX код'),
        ),
    ]
