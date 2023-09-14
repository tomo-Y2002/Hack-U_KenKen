from django.forms import Form
from django import forms

class YesNoForm(Form):
    # ラジオボタンフィールドを定義し、name属性を設定する例
    choice = forms.ChoiceField(choices=[("yes", "はい"), ("no", "いいえ")], widget=forms.RadioSelect())