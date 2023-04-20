from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # email =forms.EmailField(label="이메일")
    GENDER_CHOICES = [
        ('male', '남'),
        ('female', '여'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta(UserCreationForm.Meta):
        model =get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name','last_name')