from django import forms


class MyForm(forms.Form):
    # TODO:整数型
    # username = forms.CharField(label='ユーザー名', max_length=100)

    data = [('home appliances', 'home appliances')]
    genre = forms.ChoiceField(label='genre', choices=data)
    price_reizouko = forms.IntegerField()
    price_denshi = forms.IntegerField()
    price_sentakuki = forms.IntegerField()
