from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe  # Служит для того что бы применять теги HTML


# Register your models here.
class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_product_count')
    prepopulated_fields = {'slug': ('title',)}  # Указал от какого поля будит Автоматически заполнятся полу slug

    # Метод который позволит видеть количество товаров каждой категории
    def get_product_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))  # Получаю все продукты в списке узнаю длинну и превращаю в строку
        else:
            return '0'

    get_product_count.short_description = 'Количество товаров'  # Дали краткое описания что ыб отображалось на русском

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color', 'get_photo')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'quantity', 'size', 'color', 'category')  # То что можно редактировать
    list_display_links = ('title',)  # То на что можно кликать
    list_filter = ('title', 'price', 'category')  # То по чему я смогу фильтровать
    inlines = [GalleryInline]

    def get_photo(self, obj):  # Метод позволяющтй показать картинку товара в Админке
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Картинка'



admin.site.register(Gallery)
admin.site.register(Review)
