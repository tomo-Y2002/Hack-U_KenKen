from django.forms import ModelForm
from .models import Person

class PersonRegistrationForm(ModelForm):
    class Meta:
        model=Person
        fields=['name']#,'image']

