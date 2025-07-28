from django import template
from menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    if not request:
        return {'menu_items': [], 'current_url': ''}

    current_url = request.path
    
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
        menu_items = list(menu.items.all())
    except Menu.DoesNotExist:
        return {'menu_items': [], 'current_url': current_url}
    
    tree = build_menu_tree(menu_items, current_url)
    
    return {
        'menu_items': tree,
        'current_url': current_url,
        'request': request,
    }


def build_menu_tree(menu_items, current_url):
    items_by_parent = {}
    for item in menu_items:
        parent_id = item.parent_id
        items_by_parent.setdefault(parent_id, []).append(item)
    
    active_item = None
    for item in menu_items:
        if item.get_url() == current_url:
            active_item = item
            break
    
    active_path = set()
    if active_item:
        current = active_item
        while current:
            active_path.add(current.id)
            current = current.parent
    
    def build_tree_level(parent_id=None, level=0):
        children = items_by_parent.get(parent_id, [])
        result = []
        for item in children:
            item.is_active = (active_item and item.id == active_item.id)
            item.is_expanded = item.id in active_path
            item.level = level
            item.children_list = build_tree_level(item.id, level + 1)
            item.show_children = item.is_expanded or item.is_active
            result.append(item)
        return result
    
    return build_tree_level()
