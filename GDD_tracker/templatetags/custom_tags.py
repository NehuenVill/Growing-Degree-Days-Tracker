from django import template

register = template.Library()

@register.filter(name='get_dates')
def get_dates(value, arg):

    Val = value
    
    dts = Val[arg]["DATES"]

    return dts

@register.filter(name='get_GDD')
def get_GDD(value, arg):

    Val = value
    
    GDDs = Val[arg]["GDDAC"]

    return GDDs