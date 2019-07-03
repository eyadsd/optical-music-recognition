from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # ex: /music/
    path('', views.IndexView.as_view(), name='index'),

    path('register/', views.UserView.as_view(), name='register'),

    # ex: /music/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # ex: /music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name='album-add'),

    # ex: /music/album/2/
    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='album-update'),

    # ex: /music/album/2/delete/
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album-delete'),

]

