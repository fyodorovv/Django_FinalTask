# Generated by Django 5.0.1 on 2024-02-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_is_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='promo_text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Промо текст'),
        ),
    ]
