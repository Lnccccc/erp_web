from django import forms
from django.contrib.auth.models import User
from .models import Profile,WeixinUser

# class LoginForm(forms.Form):
#     username= forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password',widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username','first_name','email')
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError("Passwords don't match")
#         return cd['password2']

class WxUserEditForm(forms.ModelForm):
    class Meta:
        fields = WeixinUser
        fields='__all__'


class ProfileEditForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'class':'form-control'})
        self.fields['realname'].widget.attrs.update({'class':'form-control'})
    class Meta:
        model=Profile
        fields=['company','realname']


class SearchForm(forms.Form):
    search_name=forms.CharField()
