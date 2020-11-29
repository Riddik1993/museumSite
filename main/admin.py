from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import Exhibition,Exhibit,Feedback,CommentExhibition,MainInfo, \
New,Profile,Contact,NewType,PhotoNew,PhotoExhibit



nec_models=[Exhibition,CommentExhibition,MainInfo,Contact,NewType]
for m in nec_models:
    admin.site.register(m)

class FeedbackAdmin(admin.ModelAdmin):
    list_display=('user_name','description','email','pub_date','publish')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'image']


class PhotoNewInline(admin.StackedInline):
    model=PhotoNew

class NewAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    inlines = (PhotoNewInline, )

class PhotoExhibitInline(admin.StackedInline):
    model=PhotoExhibit

class ExhibitAdmin(admin.ModelAdmin):
    list_display = ['name', 'exhibition']
    list_filter = ('exhibition',)
    search_fields = ['short_description','description']
    inlines = (PhotoExhibitInline, )

admin.site.register(Exhibit,ExhibitAdmin)


class ProfileInline(admin.StackedInline):
    model=Profile

# Define a new User admin
class UserAdmin2(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin2)
admin.site.register(New, NewAdmin)
admin.site.register(Feedback,FeedbackAdmin)
