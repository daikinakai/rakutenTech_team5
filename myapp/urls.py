from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path('', views.input_view, name='home'),
    path('price/',views.price_view, name='price_page'),
    path('view/', views.success_view, name='view_page'),
    path('confirm/', views.confirm_view, name='confirm_page'),
]