from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User

class CustomUserCreationForm(UserCreationForm):
    # email =forms.EmailField(label="이메일")
    # GENDER_CHOICES = [
    #     ('male', '남'),
    #     ('female', '여'),
    # ]
    # gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = User
        fields = ('username','password1','password2','gender',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')