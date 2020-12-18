from django.urls import path

from . import views

urlpatterns = [
    # path('', views.douban_firstpage, name='douban_firstpage'),
    path('',views.index_page,name='index_page')
]