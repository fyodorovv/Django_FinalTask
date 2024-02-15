from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="Slug")
    description = models.TextField(
        blank=True, verbose_name="Подробное описание")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    count = models.IntegerField(verbose_name="Количество", default=0)
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (
        bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name="Статус")
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, related_name='products', verbose_name="Категория")

    is_promotion = models.BooleanField(
        default=False, verbose_name="Промо карусель")
    promo_text = models.CharField(
        max_length=200, blank=True, verbose_name="Промо текст")
    # promo_img = models.ImageField(upload_to='promo_img', blank=True, verbose_name="Промо картинка")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Category(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class Basket(models.Model):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.title}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        total_quantity = 0
        for basket in baskets:
            total_quantity += basket.quantity
        return total_quantity

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        total_sum = 0
        for basket in baskets:
            total_sum += basket.sum()
        return total_sum
