from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, arg):
    """
    Adds CSS class to form fields
    Usage: {{ form.field|add_class:"form-control" }}
    """
    css_classes = value.field.widget.attrs.get("class", "")
    # Only add the class if it's not already there
    if css_classes:
        if arg not in css_classes:
            css_classes = "%s %s" % (css_classes, arg)
    else:
        css_classes = arg

    return value.as_widget(attrs={"class": css_classes})
