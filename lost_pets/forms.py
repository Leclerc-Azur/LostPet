from django import forms
from .models import LostAnimal

class LostAnimalForm(forms.ModelForm):
    """Форма добавления объявления о пропавшем животном."""
    class Meta:
        model = LostAnimal
        fields = [
            'title',
            'category',
            'phone',
            'description',
            'cover',    # вместо photo
            'city',
            'district', # не забудьте, если вы добавили это поле
            'address',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }