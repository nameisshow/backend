from django.urls import path

from backend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('button/', views.button_list, name='button'),
    path('button/<int:page>/', views.button_list, name='button'),
    path('button_edit/<int:pk>/', views.button_edit, name='button_edit'),
    path('button_delete/<int:pk>/', views.button_delete, name='button_delete'),
    path('button_add/', views.button_add, name='button_add'),
    path('module/', views.module_list, name='module'),
    path('module/<int:page>/', views.module_list, name='module_list'),
    path('module_add/', views.module_add, name='module_add'),
    path('module_edit/<int:pk>/', views.module_edit, name='module_edit'),
    path('module_delete/<int:pk>/', views.module_delete, name='module_delete'),
    path('module_assign_button/<int:pk>/', views.module_assign_button, name='module_assign_button')
]
