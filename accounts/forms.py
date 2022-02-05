from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя',
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль',
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user_list = User.objects.filter(username=username)

            if not user_list.exists():
                raise forms.ValidationError('Такого пользователя не существует')

            if not check_password(password, user_list[0].password):
                raise forms.ValidationError('Неверный пароль')

            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('Данный пользователь неактивен')

        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя',
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль',
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердтие пароль',
    }))

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        data = self.cleaned_data

        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return data['password2']
