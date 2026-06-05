from django.conf import settings
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=TimberProduct.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagProduct(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Тег')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['tag']

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Supplier(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название поставщика')
    city = models.CharField(max_length=100, verbose_name='Город')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Опыт работы, лет')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.city}'


class TimberProduct(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название материала')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name='Статус публикации',
    )
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория',
    )
    tags = models.ManyToManyField(
        TagProduct,
        blank=True,
        related_name='products',
        verbose_name='Теги',
    )
    supplier = models.OneToOneField(
        Supplier,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='product',
        verbose_name='Поставщик',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='timber_products',
        verbose_name='Автор',
    )
    wood_type = models.CharField(max_length=100, verbose_name='Порода древесины')
    size = models.CharField(max_length=100, verbose_name='Размер')
    grade = models.CharField(max_length=100, verbose_name='Сорт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ориентировочная цена')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Карточка пиломатериала'
        verbose_name_plural = 'Карточки пиломатериалов'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Comment(models.Model):
    product = models.ForeignKey(
        TimberProduct,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Карточка материала',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст комментария')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.product}'


class Reaction(models.Model):
    class Value(models.IntegerChoices):
        DISLIKE = -1, 'Дизлайк'
        LIKE = 1, 'Лайк'

    product = models.ForeignKey(
        TimberProduct,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name='Карточка материала',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name='Пользователь',
    )
    value = models.SmallIntegerField(choices=Value.choices, verbose_name='Реакция')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Реакция'
        verbose_name_plural = 'Реакции'
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_user_product_reaction'),
        ]

    def __str__(self):
        return f'{self.user}: {self.get_value_display()} для {self.product}'