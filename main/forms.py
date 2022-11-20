from django import forms
from main import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ImageCaptionForm(forms.ModelForm):
    class Meta:
        model = models.ImageCaption
        fields = ('img', )


class machine_translation_form(forms.ModelForm):

    class Meta:
        model = models.machine_translation
        fields = '__all__'  # include = ('name', 'roll_no')


class Article_finder_form(forms.ModelForm):

    class Meta:
        model = models.article_finder
        fields = '__all__'  # include = ('name', 'roll_no')


class asset_transport_req_form(forms.ModelForm):

    class Meta:
        model = models.asset_transport_request_model
        fields = '__all__'


class share_travel_information_form(forms.ModelForm):

    class Meta:
        model = models.share_travel_information_model
        fields = '__all__'


# class Sign_in_form(forms.ModelForm):

#     class Meta:
#         model = models.signin_data
#         # widgets = {
#         #     'password': forms.PasswordInput(),
#         # }
#         fields = '__all__'  # include = ('name', 'roll_no')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
