from django.forms import ModelForm,Form
from .models import Person
from django import forms




class PersonRegistrationForm(ModelForm):
    class Meta:
        model=Person
        fields=['family_name','first_name','email','birthday','image']

class YesNoForm(Form):
    # ラジオボタンフィールドを定義し、name属性を設定する例
    choice = forms.ChoiceField(choices=[("yes", "はい"), ("no", "いいえ")], widget=forms.RadioSelect())