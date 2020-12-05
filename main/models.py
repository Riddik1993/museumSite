from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from embed_video.fields import EmbedVideoField




agree_choices=[('Y','Да'),('N','Нет')]

#модель, расширяющая данные о пользователе
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(max_length=1000, blank=True,verbose_name="Биография")
    birth_date=models.DateField(null=True, blank=True,verbose_name="Дата рождения")
    photo=models.ImageField(upload_to='images/profiles',blank=True,verbose_name="Фото")
    position=models.CharField(max_length=150,blank=True,verbose_name='должность')
    show_on_admin=models.CharField('Отображать в администрации музея?',max_length=3,choices=agree_choices,default='N')

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'

#создаем менеджер модели для реализации поиска
class ContentManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(name__icontains=query) | Q(description__icontains=query))
            qs = qs.only('name','description').filter(or_lookup)
        return qs

#абстрактные модели для статей и отзывов
class ContentObject(models.Model):
    name=models.CharField(max_length=100,verbose_name='Название')
    description=models.TextField(blank=True,verbose_name='Описание')
    pub_date=models.DateField(max_length=100,auto_now_add=True,verbose_name='Дата_публикации')
    objects=ContentManager()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class CommentObject(models.Model):
    user_name=models.CharField(max_length=100,verbose_name='Имя_пользователя')
    description=models.TextField(blank=True,verbose_name='Текст')
    email=models.EmailField(verbose_name='Email')
    pub_date=models.DateField(auto_now_add=True,verbose_name='Дата_публикации')
    publish=models.CharField('Публиковать?',max_length=3,choices=agree_choices,default='N')

    def __str__(self):
        return self.description[:40]

    class Meta:
        abstract = True



class Exhibition(ContentObject):

    def get_absolute_url(self):
        return f"/exhibition/{self.id}"

    class Meta:
        verbose_name='Выставка'
        verbose_name_plural='Выставки'


class ContentPhoto(models.Model):
    subject=models.ForeignKey('Exhibit',null=True,on_delete=models.PROTECT,verbose_name='exhibit_photo')
    image=models.ImageField(upload_to=f'images/{subject.verbose_name}',verbose_name='Фотография')
    main_photo=models.CharField('Главное фото?',max_length=3,choices=agree_choices,default='N')


    class Meta:
        abstract = True
        verbose_name='Фото'

class Exhibit(ContentObject):
    short_description=models.TextField(max_length=70,blank=True,verbose_name='Краткое описание')
    exhibition=models.ForeignKey('Exhibition',null=True,on_delete=models.PROTECT,verbose_name='Выставка')

    def get_absolute_url(self):
        return f"/exhibit/{self.id}"
    def get_photo_url(self):
        return PhotoExhibit.objects.get(subject=self.id,main_photo='Y')

    class Meta:
        verbose_name='Экспонат'
        verbose_name_plural='Экспонаты'

class PhotoExhibit(ContentPhoto):

    class Meta:
        verbose_name='Фото экспоната'
        verbose_name_plural='Фото экспоната'

class Contact(ContentObject):
    telephone=models.CharField(max_length=50,verbose_name='Номер телефона')
    email=models.EmailField(verbose_name='Email',blank=True)

    class Meta:
        verbose_name='Контакт'
        verbose_name_plural='Контакты'


class MainInfo(ContentObject):
    image1=models.ImageField(upload_to='images/mainpage',blank=True,verbose_name='Картинка1')
    image2=models.ImageField(upload_to='images/mainpage',blank=True,verbose_name='Картинка2')

    class Meta:
        verbose_name='Инфо на главной странице'
        verbose_name_plural='Инфо на главной странице'

class CommentExhibition(CommentObject):
    exhibition=models.ForeignKey('Exhibition',null=True,on_delete=models.PROTECT,verbose_name='Выставка')
    class Meta:
        verbose_name='Комментарий по выставке'
        verbose_name_plural='Комментарии по выставке'

class Feedback(CommentObject):

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'

class New(ContentObject):
    type=models.ForeignKey('NewType',blank=True,null=True,on_delete=models.PROTECT,verbose_name='Тип новости')
    short_description=models.TextField(max_length=70,blank=True,verbose_name='Краткое описание')
    hot_new=models.CharField('Важная новость?',max_length=3,choices=agree_choices,default='N')
    video = EmbedVideoField(blank=True,verbose_name='Ссылка на видео')

    def get_absolute_url(self):
        return f"/news/{self.id}"
    def get_photo_url(self):
        return PhotoNew.objects.get(subject=self.id,main_photo='Y')

    class Meta:
        verbose_name='Новость'
        verbose_name_plural='Новости'

class PhotoNew(ContentPhoto):
    subject=models.ForeignKey('New',null=True,on_delete=models.CASCADE,
                                verbose_name='new_photo',related_name='images')
    image=models.ImageField(upload_to='images/new_photo',verbose_name='Фотография')

    class Meta:
        verbose_name='Фото для новости'
        verbose_name_plural='Фото для новости'



class NewType(ContentObject):
    objects=models.Manager()
    publish=models.CharField('Отображать в меню сайта?',max_length=3,choices=agree_choices,default='Y')
    class Meta:
        verbose_name='Тип новости'
        verbose_name_plural='Типы новостей'







# Create your models here.
