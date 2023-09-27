from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime
from .forms import MyForm

# Create your views here.
# class Home(TemplateView):
#     template_name = "myapp/home.html"

def success_view(request):
    # 入力値をコンテキストに追加
    params = {}
    params['genre'] = request.GET.get("genre")
    params['price_reizouko'] = request.GET.get("price_reizouko")
    params['price_denshi'] = request.GET.get("price_denshi")
    params['price_sentakuki'] = request.GET.get("price_sentakuki")
    # densirenjiPrice,reizoukoPrice,sentakutukiPrice = request.GET.get('densirenjiPrice', 'reizoukoPrice',"sentakukiPrice")
    return render(request, 'myapp/views.html', params)


def input_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # フォームがバリデーションを通過した場合、データを処理
            params = {}
            params['genre'] = form.cleaned_data['genre']
            params['price_reizouko'] = form.cleaned_data['price_reizouko']
            params['price_denshi']  = form.cleaned_data['price_denshi']
            params['price_sentakuki'] = form.cleaned_data['price_sentakuki']
            # データを使用して何かを行います
            # return redirect('myapp:view_page')  # データが正常に処理された場合、リダイレクト
            return render(request, 'myapp/views.html',params)
    else:
        form = MyForm()  # GETリクエストの場合、空のフォームを表示
    return render(request, 'myapp/home.html', {'form': form})