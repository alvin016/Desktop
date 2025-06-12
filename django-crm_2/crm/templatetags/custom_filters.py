from django import template

register = template.Library()

@register.filter
def get_item(queryset, pk):
    return queryset.filter(pk=pk).first()