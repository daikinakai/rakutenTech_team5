from typing import Any
from django import forms
from django.core.exceptions import ValidationError


class MyForm(forms.Form):
    # TODO:整数型
    # username = forms.CharField(label='ユーザー名', max_length=100)

    data = [("home appliances", "home appliances")]
    genre = forms.ChoiceField(label="genre", choices=data)
    price_reizouko = forms.IntegerField()
    price_denshi = forms.IntegerField()
    price_sentakuki = forms.IntegerField()
    price_suihanki = forms.IntegerField()
    price_television = forms.IntegerField()
    price_soujiki = forms.IntegerField()
    price_hair_dryer = forms.IntegerField()


class CheckForm(forms.Form):
    data = [("home appliances", "home appliances")]
    genre = forms.ChoiceField(label="genre", choices=data)

    home_appliances_choices = [
        ("refrigerator_price", "refrigerator"),
        ("microwave_oven_price", "microwave oven"),
        ("washing_machine_price", "washing machine"),
        ("rice_cooker_price", "rice cooker"),
        ("television_price", "television"),
        ("Vacuum_cleaner_price", "vacuum cleaner"),
        ("hair_dryer_price", "hair dryer"),
    ]

    Need_items = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=home_appliances_choices,
    )

    def clean(self):
        super().clean()
        entries = self.cleaned_data
        if len(entries["Need_items"]) != 3:
            raise ValidationError("最大で3つまで選択できます。")
        return entries


class PriceForm(forms.Form):
    pass
