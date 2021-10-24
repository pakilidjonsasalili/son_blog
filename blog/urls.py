from django.urls import path
from . import views


app_name = 'blog'
urlpatterns=[
    #chamar view listar_posts
    path('', views.ListarPostsView.as_view(), name='listar_posts'),
    path('<slug:slug>/',
         views.DetalharPostView.as_view(), name='detalhe'),
    path('sharepost/<int:pk>/', views.FormContatoView.as_view(), name='share_post'),
    path('comentarpost/<int:pk>', views.ComentarioView.as_view(), name='comentar_post'),
    path('cadastrousuario', views.CadUsuarioView.as_view(), name='cadastrouser'),
    path('loginuser', views.LoginUsuarioView.as_view(), name='loginuser'),
    path('logoutuser', views.LogoutUsuarioView.as_view(), name='logoutuser'),
]