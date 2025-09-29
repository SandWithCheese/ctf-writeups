from django import forms
from django.contrib.auth.models import User
from .models import Profile, Menfess
from django.core.exceptions import ValidationError

blacklist = ["{{","}}",".","*",">","<","import","popen","read","application","/","flag","globals","getitem","echo",'"',"cat","+","lipsum","getattr","joiner","namespace","dict","range","cycler","request","self","config",'\\',"0x","bytes","0o","0b","os","lower","upper"]

def validate(bio):
    if not bio.isascii():
        raise ValidationError("Bio can only be ascii characters")
    else:
        for char in blacklist:
            if char in bio:
                raise ValidationError("Your bio contains prohibited characters")

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('Username already taken')
        return u


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
    
    bio = forms.CharField(
        required=False,
        validators=[validate]
    )


class MenfessForm(forms.ModelForm):
    class Meta:
        model = Menfess
        fields = ['recipient', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }
