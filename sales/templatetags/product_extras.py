from django import template

register = template.Library()

@register.filter
def get_images(product):
    return [img for img in [product.image_1, product.image_2, product.image_3, product.image_4] if img]
