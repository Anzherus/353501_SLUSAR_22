from django import template

register = template.Library()


@register.filter(name='split_lines')
def split_lines(value):
    """Split a multiline text field into a list of non-empty trimmed lines."""
    if not value:
        return []
    if not isinstance(value, str):
        try:
            value = str(value)
        except Exception:
            return []
    lines = [line.strip('-• \t').strip() for line in value.replace('\r\n', '\n').split('\n')]
    return [line for line in lines if line]


