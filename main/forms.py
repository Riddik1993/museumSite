from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm





class FeedbackForm(ModelForm):
    captcha=CaptchaField(label='Текст с картинки',error_messages={'invalid': 'Неверный текст с картинки!'})
    class Meta:
        model=Feedback
        fields=('user_name','email','description')
