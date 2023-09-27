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

APPLICATION_ID = "1098599347371457724"

RANK_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"


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
            return render(request, 'myapp/views.html', {'data': data })
    else:
        form = MyForm()  # GETリクエストの場合、空のフォームを表示
    return render(request, 'myapp/home.html', {'form': form})

def api(params):
    ITEM_GENRE_ID = {
        'reizouko': 565161,
        'sentakuki': 204491,
        'denshi': 204585
    }
    
    products_info = {
        'reizouko': get_products_info(params['price_reizouko'], ITEM_GENRE_ID['reizouko'], 'limit'),
        'sentakuki':get_products_info(params['price_sentakuki'], ITEM_GENRE_ID['sentakuki'], 'limit'),
        'denshi': get_products_info(params['price_denshi'], ITEM_GENRE_ID['denshi'], 'limit')
    }

    return products_info
    

def get_products_info(price, genre_id, sort):
    
    products = []

    query_params = {
        "genreId": genre_id,
        "elements": "itemName,itemUrl,itemPrice,mediumImageUrls",
        "applicationId": APPLICATION_ID,
    }
    try:
        product_response = requests.get(RANK_API, params=query_params)
        if product_response.status_code == 200:
            product_data = product_response.json()
            processed_data = None
            if (sort == 'limit'):
                data_filtered_by_prices = [x for x in product_data["Items"] if int(x['Item']['itemPrice']) <= price]
                processed_data = sorted(data_filtered_by_prices, key=lambda x: x['Item']['itemPrice'], reverse=True)
            else:
                processed_data = sorted(product_data["Items"], key=lambda x: abs(int(x['Item']['itemPrice']) - price))
            
            for item in processed_data:
                product = {
                    'name': item['Item']['itemName'],
                    'url': item['Item']['itemUrl'],
                    'price': item['Item']['itemPrice'],
                    'image_url': item['Item']['mediumImageUrls'][0]['imageUrl']
                }
                products.append(product)
            return products
             
               
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Request Error: {e}"}, status=500)