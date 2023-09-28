from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .forms import CheckForm, PriceForm, MyForm
from django import forms
import time

APPLICATION_ID = "1098599347371457724"

RANK_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"


def success_view(request):
    if request.method == "POST":
        params = {}
        params["genre"] = request.POST.get("genre")
        params["price_reizouko"] = request.POST.get("price_reizouko")
        params["price_denshi"] = request.POST.get("price_denshi")
        params["price_sentakuki"] = request.POST.get("price_sentakuki")
        params["price_suihanki"] = request.POST.get("price_suihanki")
        params["price_television"] = request.POST.get("price_television")
        params["price_soujiki"] = request.POST.get("price_soujiki")
        params["price_hair_dryer"] = request.POST.get("price_hair_dryer")

        data = api(params)

        return render(request, "myapp/views.html", {"data": data})


# def input_view(request):
#     params = {
#         'headtitle' : 'team5',
#         'title' : 'Select genre & budget!',
#         'form' : CheckForm(),
#         'btn' : 'select',
#     }

#     if request.method == 'POST':
#         keys = request.POST.keys()
#         if 'genre' in keys and 'Need_items' in keys:
#             form = CheckForm(request.POST)
#             if form.is_valid():
#                 params = {
#                     'headtitle' : 'team5',
#                     'title' : 'Select genere & budget!',
#                     'btn' : 'get recommend',
#                 }
#                 temp = form.cleaned_data.get('Need_items')

#                 dyn_form = PriceForm()
#                 for k in temp:
#                     dyn_form.fields[k.replace('_',' ')] = forms.IntegerField(\
#                                 min_value=0)
#                 dyn_form.fields['budget_over'] = forms.BooleanField(required=False)
#                 params['form'] = dyn_form
#                 return render(request, 'myapp/home.html', params)
#             else:

#                 return render(request, 'myapp/home.html', params)
#         # 金額入力
#         elif 'refrigerator price' in keys\
#             or 'microwave oven price' in keys\
#                 or 'washing machine price' in keys:

#             for k in keys:
#                 if k != 'csrfmiddlewaretoken':
#                     params[k] = request.POST[k]


#             params['title'] = 'view_list'
#             params['headtitle'] = 'team5'
#             del params['form'], params['btn']

#             return redirect('myapp:view_page')


#     else:
#         return render(request, 'myapp/home.html', params)
def input_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # データが正常に処理された場合、リダイレクト
            return redirect("myapp:view_page")
    else:
        form = MyForm()  # GETリクエストの場合、空のフォームを表示

    return render(request, "myapp/home.html", {"form": form})


def api(params):
    ITEM_GENRE_ID = {
        "reizouko": 565161,
        "sentakuki": 204491,
        "denshi": 204585,
        "suihanki": 204586,
        "television": 563843,
        "soujiki": 204492,
        "hair_dryer": 502792,
    }

    products_info = {}
    for i, name in enumerate(list(ITEM_GENRE_ID.keys())):
        products_info[name] = get_products_info(params[f"price_{name}"], ITEM_GENRE_ID[name], "limit")
        if i % 3 == 0:
            time.sleep(1)

    return products_info


def get_products_info(price, genre_id, sort):
    price = int(price)

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
            if sort == "limit":
                data_filtered_by_prices = list(
                    filter(lambda x: int(x["Item"]["itemPrice"]) <= price, product_data["Items"])
                )
                processed_data = sorted(data_filtered_by_prices, key=lambda x: abs(int(x["Item"]["itemPrice"]) - price))
            else:
                processed_data = sorted(product_data["Items"], key=lambda x: abs(int(x["Item"]["itemPrice"]) - price))

            for item in processed_data:
                product = {
                    "name": item["Item"]["itemName"],
                    "url": item["Item"]["itemUrl"],
                    "price": item["Item"]["itemPrice"],
                    "image_url": item["Item"]["mediumImageUrls"][0]["imageUrl"],
                }
                products.append(product)
            return products

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Request Error: {e}"}, status=500)
