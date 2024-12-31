from django import template
from user.models import PartTopic  # O'zingizning ilova nomingizni qo'shing

register = template.Library()

@register.filter
def get_item(queryset, item_id):
    print("Filter called with:", queryset, item_id)
    try:
        return queryset.get(id=item_id).topic
    except PartTopic.DoesNotExist:
        return "Unknown Topic"
