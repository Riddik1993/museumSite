from .models import Exhibition,NewType
from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#формирование меню
def get_menu():
    context={}
    newstypes=cache.get('newstypes')
    if not newstypes:
        newstypes=NewType.objects.only('name').filter(publish='Y')
        cache.set('newstypes',newstypes,60*2)
    expositions=cache.get('expositions')
    if not expositions:
        expositions=Exhibition.objects.all().only('name')
        cache.set('expositions',expositions,60*2)


    context['newstypes']=newstypes
    context['exp']=expositions
    return context

#пагинация объектов на странице
def paginate(request,full_list,pages):
    current_page=request.GET.get('page')
    paginator=Paginator(full_list,pages)
    try:
        object_list=paginator.page(current_page)
    except EmptyPage:
        object_list=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        object_list=paginator.page(1)
    return object_list
