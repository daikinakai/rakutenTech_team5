from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime, requests
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
            data = api(params)
            # データを使用して何かを行います
            # return redirect('myapp:view_page')  # データが正常に処理された場合、リダイレクト
            return render(request, 'myapp/views.html', {'data': data})
    else:
        form = MyForm()  # GETリクエストの場合、空のフォームを表示
    return render(request, 'myapp/home.html', {'form': form})

def api(params):
    ITEM_GENRE_ID = {
        'reizouko': 565161,
        'sentakuki': 204491,
        'denshi': 204585
    }

    APPLICATION_ID = "1098599347371457724"

    RANK_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
    ITEM_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

    # Define the query parameters to get rezouko information
    reizouko_params = {
        "genreId": ITEM_GENRE_ID['reizouko'],
        "maxPrice": params['price_reizouko'],
        "elements": "itemCode,itemName,itemUrl,itemPrice,mediumImageUrls",
        "applicationId": APPLICATION_ID,
        "sort": "-itemPrice" # Sort by price in descending order 
    }

    try:
        reizouko_response = requests.get(ITEM_API, params=reizouko_params)
        if reizouko_response.status_code == 200:
            reizouko_data = reizouko_response.json()
            return reizouko_data["Items"]
                        
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Request Error: {e}"}, status=500)
