from django.urls import path

from backend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('button/', views.button_list, name='button'),
    path('button/<int:page>/', views.button_list, name='button'),
    path('button_edit/<int:pk>/', views.button_edit, name='button_edit')
]
