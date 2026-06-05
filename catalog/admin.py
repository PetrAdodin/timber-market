from django.contrib import admin

from .models import Category, Comment, Reaction, Supplier, TagProduct, TimberProduct


@admin.register(TimberProduct)
class TimberProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'cat',
        'author',
        'wood_type',
        'grade',
        'price',
        'is_published',
        'time_create',
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published', 'price')
    ordering = ('-time_create', 'title')
    list_per_page = 10
    search_fields = ('title', 'content', 'wood_type', 'size', 'grade')
    list_filter = ('is_published', 'cat', 'wood_type', 'grade', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ('time_create', 'time_update')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TagProduct)
class TagProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'experience_years')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'city')
    list_filter = ('city',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'author', 'time_create', 'is_active')
    list_display_links = ('id', 'product')
    search_fields = ('text', 'author__username', 'product__title')
    list_filter = ('is_active', 'time_create')
    readonly_fields = ('time_create',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'value', 'time_create')
    list_display_links = ('id', 'product')
    search_fields = ('product__title', 'user__username')
    list_filter = ('value', 'time_create')
    readonly_fields = ('time_create',)


admin.site.site_header = 'Администрирование Timber Market'
admin.site.index_title = 'Панель управления каталогом пиломатериалов'