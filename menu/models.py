from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'menu'
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, verbose_name="Title")
    url = models.CharField(max_length=200, blank=True, verbose_name="URL")
    named_url = models.CharField(max_length=100, blank=True, verbose_name="Named URL")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    

    class Meta:
        db_table = 'menu_item'
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')
        ordering = ['order', 'id']

    
    def __str__(self):
        return self.title
    
    def get_url(self):
        """Get the URL for this menu item"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'
