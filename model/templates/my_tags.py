from atexit import register
from django import template
from django.utils.safestring import mark_safe
register=template.Library()
@register.filter
def image(v1):
  f=v1.replace(' ','_')
  return 'images/'+f+'.png'
@register.filter
def category_image(v1):
  return 'images/home_imag/'+v1+'.svg'
@register.filter
def model_(v1):
  f=v1.replace(' ','_')
  return 'model/'+f+'.glb'
@register.filter
def gif_(v1):
  f=v1.replace(' ','_')
  return 'images/home_imag/'+f+'.gif'
@register.filter(is_safe=True)
def label_with_classes(value, arg):

    return value.label_tag(attrs={'class': arg})