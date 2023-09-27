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
    username = request.GET.get("username")
    # densirenjiPrice,reizoukoPrice,sentakutukiPrice = request.GET.get('densirenjiPrice', 'reizoukoPrice',"sentakukiPrice")
    return render(request, 'myapp/views.html', {'username': username,})


def input_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # フォームがバリデーションを通過した場合、データを処理
            username = form.cleaned_data['username']
            # データを使用して何かを行います
            return redirect('myapp:view_page')  # データが正常に処理された場合、リダイレクト
    else:
        form = MyForm()  # GETリクエストの場合、空のフォームを表示
    return render(request, 'myapp/home.html', {'form': form})