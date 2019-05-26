from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email", required=True,
                             help_text='Required. Inform a valid email address.')

    name = forms.CharField(label="Name", required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'email')

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email already exists.')
        else:
            return email

    def save_all(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user