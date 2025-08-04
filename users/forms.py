from django import forms
from .models import MyUser

class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя с подтверждением пароля."""
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user