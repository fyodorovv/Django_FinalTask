# Generated by Django 5.0.1 on 2024-02-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='product',
            name='promo_text',
            field=models.CharField(blank=True, max_length=100, verbose_name='Промо текст'),
        ),
    ]
