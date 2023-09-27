from django import forms


class MyForm(forms.Form):
    # TODO:整数型
    username = forms.CharField(label='ユーザー名', max_length=100)
    price_reizouko = forms.IntegerField()
    # price_denshi = 
    # price_sentakuki = 
