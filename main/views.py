from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from .models import *
from .forms import *
from django.views.generic import TemplateView
from itertools import chain
from .utils import get_menu,paginate
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import JsonResponse
from django.core.cache import cache

def ShowMP(request):
    context=get_menu()
    news=cache.get('news')
    if not news:
        news=New.objects.only('name','short_description','hot_new').all().\
                        order_by('-pub_date')[:5]
        cache.set('news',news,60)

    mainInfo=cache.get('mainInfo')
    if not mainInfo:
        mainInfo=MainInfo.objects.only('name','description','image1',).first()
        cache.set('mainInfo',mainInfo,60)
    context['info']=mainInfo
    context['news']=news
    return render(request, "main/mainpage.html",context)

@cache_page(30)
def ShowNewPage(request,new_id):
    context=get_menu()
    new=New.objects.only('name','description').get(id=new_id)
    context['new']=new

    return render(request, "main/news_page.html",context)

@cache_page(30)
def ShowExhibition(request,ex_id):
    context=get_menu()
    context['exhibition']=Exhibition.objects.get(id=ex_id)
    context['exh_list']=Exhibit.objects.only('name','short_description').filter(exhibition_id=ex_id)
    return render(request, "main/exhibition.html",context)

@cache_page(30)
def ShowExhibit(request,exh_id):
    exp=Exhibition.objects.all().only('name','description')
    subj=Exhibit.objects.only('name','description').get(id=exh_id)
    photo=PhotoExhibit.objects.get(subject=subj,main_photo="Y")
    return render(request, "main/exhibit.html",{'subj':subj,'exp':exp,'photo':photo})

def ShowSuccessFeedback(request):
    context=get_menu()
    return render(request, "main/success_feedback.html",context)

def ShowFeedB(request):
    context=get_menu()
    feed_list=cache.get('feed_list')
    if not feed_list:
        feed_list=Feedback.objects.all().only('user_name','description',
                                            'pub_date').filter(publish='Y').order_by('-pub_date')
        cache.set('feed_list',feed_list,60*5)
    feedbacks_list=feed_list

    context['feedbacks']=paginate(request,feedbacks_list,4)

    if request.method=='POST':
       form = FeedbackForm(request.POST)
       context['form']=form
       if form.is_valid():
           fb=form.save(commit=False)
           fb.save()
           return redirect('success_feedback')
       else:
           return render(request, "main/feedback.html", context)
    else:
        context['form']= FeedbackForm()
        return render(request, "main/feedback.html", context)

@cache_page(60)
def ShowAdminContacts(request):
    context=get_menu()
    context['admins']=Profile.objects.only('position','photo').filter(show_on_admin='Y')
    return render(request,"main/administration.html",context)

def SendEmpBio(request):
    id = int(request.GET['id'])
    person=Profile.objects.only('bio').get(id=id)
    bio_text=person.bio
    return HttpResponse(bio_text)

#реализация поиска
class SearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        context=get_menu()
        q = request.GET.get('q')
        if q:
            query_sets = []  # Общий QuerySet
            # Ищем по  моделям
            query_sets.append(Exhibition.objects.search(query=q))
            query_sets.append(Exhibit.objects.search(query=q))
            query_sets.append(New.objects.search(query=q))
            # и объединяем выдачу
            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.pub_date, reverse=True)  # Выполняем сортировку

            context['last_question'] = f'q={q}'
            context['object_list']=paginate(request,final_set,5)
        return render(request=request, template_name='main/search_result.html'
                    , context=context)

def ShowContact(request):
    context=get_menu()
    context['contacts']=Contact.objects.all()
    return render(request,"main/contact.html",context)

def ShowDirections(request,dir_id):
    context=get_menu()
    news=New.objects.only('name','short_description').filter(type=dir_id)
    context['news']=paginate(request,news,4)
    return render(request,"main/directions.html",context)

def ShowNewInfoAjax(request):
    id = int(request.GET['id'])
    subj=New.objects.get(id=id)
    photos=list(PhotoNew.objects.filter(subject=subj).only('image').values())
    photo_urls=[]
    for ph in photos:
        photo_urls.append(ph['image'])
    return JsonResponse({'desc':subj.description,'photo_urls':photo_urls,
                        'video':subj.video})

def SendExhibitInfo(request):
    id = int(request.GET['id'])
    subj=Exhibit.objects.get(id=id)
    photos=list(PhotoExhibit.objects.filter(subject=subj).only('image').values())
    photo_urls=[]
    for ph in photos:
        photo_urls.append(ph['image'])
    return JsonResponse({'desc':subj.description,'photo_urls':photo_urls})
