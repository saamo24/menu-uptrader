from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ('title', 'url', 'named_url', 'parent', 'order')
    ordering = ['order', 'id']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'parent', 'order']
    list_filter = ['menu']
    list_editable = ['order']
    search_fields = ['title']
    ordering = ['menu', 'order', 'id']

