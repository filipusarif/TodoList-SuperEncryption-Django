from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-page'),

    path('delete-task/<str:id>/', views.DeleteTask, name='delete'),
    path('status/<str:id>/', views.Status, name='status'),
    path('edit/<str:id>/', views.Edit, name='edit'),
]