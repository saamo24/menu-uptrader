from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Menu


class MenuView(View):
    def get(self, request, menu_name=None, item_path=None):
        if not menu_name:
            all_menus = Menu.objects.all()
            return render(request, 'menu/menu_list.html', {'menus': all_menus})
        
        menu = get_object_or_404(Menu.objects.prefetch_related('items'), name=menu_name)
        items = list(menu.items.all())

        item_map = {item.id: item for item in items}
        tree = []

        for item in items:
            item.children_list = []
        for item in items:
            if item.parent_id:
                parent = item_map.get(item.parent_id)
                if parent:
                    parent.children_list.append(item)
            else:
                tree.append(item)

        context = {
            'menu_name': menu_name,
            'menu_items': tree,
        }
        return render(request, 'menu/menu.html', context)
