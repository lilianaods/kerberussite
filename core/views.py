from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'core/index.html')
	
def login(request):
    return render(request, 'core/login.html')

def membro_cadastrar(request):
	return render(request, 'core/register.html')
	
def membro_listar(request):
	return render(request, 'core/tables.html')
		
def relatorio_geral(request):
	return render(request, 'core/relatoriogeral.html')	
	
def relatorio_membro(request):
	return render(request, 'core/relatoriomembro.html')	
