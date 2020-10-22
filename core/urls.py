from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard'),
	path('login/', views.login, name='login'),
	path('membro/cadastro/', views.membro_cadastrar, name='registro'),
	path('membro/lista/', views.membro_listar, name='listagem'),
	path('geral/', views.relatorio_geral, name='relatoriogeral'),
	path('membro/', views.relatorio_membro, name='relatoriomembro')
]
