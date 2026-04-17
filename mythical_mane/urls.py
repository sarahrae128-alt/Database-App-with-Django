from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patients, name='patients'),
    path('visits/', views.visits, name='visits'),
    path('owners/', views.owners_list, name='owners_list'),
    path('owners/create/', views.owner_create, name='owner_create'),
    path('owners/<int:pk>/edit/', views.owner_edit, name='owner_edit'),
    path('owners/<int:pk>/delete/', views.owner_delete, name='owner_delete'),
    path('carenotes/', views.carenotes_list, name='carenotes_list'),
    path('carenotes/create/', views.carenote_create, name='carenote_create'),
    path('carenotes/<int:pk>/edit/', views.carenote_edit, name='carenote_edit'),
    path('carenotes/<int:pk>/delete/', views.carenote_delete, name='carenote_delete'),
]
