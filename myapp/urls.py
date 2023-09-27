from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path('', views.input_view, name='home'),
    path('view/', views.success_view, name='view_page'),
]