from django.contrib import admin, messages
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'price', 'count', 'promo_text',
              'image',  'description', 'category', 'is_published', 'is_promotion']
    # exclude = ['tags', 'is_published']
    # readonly_fields = ['slug']
    prepopulated_fields = {"slug": ("title", )}
    # filter_horizontal = ['tags']
    list_display = ('title', 'time_create',
                    'is_published', 'category')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Product.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Product.Status.DRAFT)
        self.message_user(
            request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
