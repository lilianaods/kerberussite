from core.models import Membro, Entrada
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

import paho.mqtt.client as mqtt
import subprocess
import time

from datetime import datetime
 
def index(request):
    return render(request, 'core/index.html')
	
def login_kerberus(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		
        user = authenticate(request, username=username, password=password)
		
        if user is not None:
           login(request, user)
           return redirect('dashboard')
		   
    return render(request, 'core/login.html')

def membro_cadastrar(request):
    cadastro = False
	
    if request.method == 'POST':
        nome = request.POST['nome'].upper()
        curso = request.POST['curso'].upper()	
        
        membro = Membro(nome=nome, curso=curso, foto=request.POST['foto'])
        membro.save()
		
        cadastro = True

    context = {'membro_cadastrado': cadastro} 

    return render(request, 'core/blank.html', context)
	
def membro_listar(request):
	membros = Membro.objects.all().order_by('nome')
	
	context = {'membros': membros}
	
	return render(request, 'core/tables.html', context)
		
def relatorio_geral(request):
	if request.method == 'POST':
		dados = request.POST.dict()
		
		data_inicial = datetime.strptime(dados['datainicial'], "%Y-%m-%d")
		data_inicial = data_inicial.replace(hour=23, minute=59)
		
		data_final = datetime.strptime(dados['datafinal'], "%Y-%m-%d")
		data_final = data_final.replace(hour=23, minute=59)	
		
		entradas = Entrada.objects.filter(data__lte=data_final, data__gte=data_inicial).order_by('data')
		
		primeira_entrada_de_cada_membro = Entrada.objects.all().distinct('membro')
		quantidade_membros = len(primeira_entrada_de_cada_membro)
		
		membros_presentes = []
		
		for entrada in primeira_entrada_de_cada_membro:
			membros_presentes.append({"nome": entrada.membro.nome, "curso": entrada.membro.curso})
					
		entradas_formatadas = []
		aux_frequencia = []
		
		for entrada in entradas:
			entradas_formatadas.append({"data": entrada.data.date().strftime("%d/%m/%Y"), "hora": entrada.data.time().strftime("%H:%M:%S"), "membro": entrada.membro.nome})
			aux_frequencia.append(entrada.data.weekday())
			
			frequencia = max(set(aux_frequencia), key = aux_frequencia.count)

		frequencia_dia = ''
		if (frequencia == 0):
			frequencia_dia = "Segunda"
		elif (frequencia == 1):
			frequencia_dia = "Terça";
		elif (frequencia == 2):
			frequencia_dia = "Quarta";
		elif (frequencia == 3):
			frequencia_dia = "Quinta";
		elif (frequencia == 4):
			frequencia_dia = "Sexta";
		elif (frequencia == 5):
			frequencia_dia = "Sábado";
		elif (frequencia == 6):
			frequencia_dia = "Domingo";	
		
		context = {}
		context['data_inicial'] = datetime.strptime(dados['datainicial'], "%Y-%m-%d").strftime('%d/%m/%Y')
		context['data_final'] = datetime.strptime(dados['datafinal'], "%Y-%m-%d").strftime('%d/%m/%Y')
		context['quantidade_membros'] = quantidade_membros
		context['membros_presentes'] = membros_presentes
		context['frequencia'] = frequencia_dia
		context['entradas'] = entradas_formatadas[:10]
		
		return render(request, 'core/relatoriogeral.html', context)	
	elif request.method == 'GET':
		return render(request, 'core/relatoriogeral.html')	
	
def relatorio_membro(request):
	membros_cadastrados = Membro.objects.all()
	ultimos_membros_cadastrados = membros_cadastrados[:5]
	
	context = {'membros_cadastrados': membros_cadastrados,
	'ultimos_membros_cadastrados': ultimos_membros_cadastrados}
	
	if request.method == 'POST':
		dados = request.POST.dict()
		
		membro_selecionado = Membro.objects.get(pk=dados["membro"])
		
		data_inicial = datetime.strptime(dados['datainicial'], "%Y-%m-%d")
		data_inicial = data_inicial.replace(hour=23, minute=59)
		
		data_final = datetime.strptime(dados['datafinal'], "%Y-%m-%d")
		data_final = data_final.replace(hour=23, minute=59)
		
		entradas = Entrada.objects.filter(data__lte=data_final, data__gte=data_inicial, membro=membro_selecionado).order_by('data')
		
		entradas_formatadas = []
		aux_frequencia = []
		aux_quantidade = []
		
		for entrada in entradas:
			entradas_formatadas.append({"data": entrada.data.date().strftime("%d/%m/%Y"), "hora": entrada.data.time().strftime("%H:%M:%S")})
			aux_frequencia.append(entrada.data.weekday())
			aux_quantidade.append(entrada.data.date().strftime("%d/%m/%Y"))
			
			frequencia = max(set(aux_frequencia), key = aux_frequencia.count)

		frequencia_dia = ''
		if (frequencia == 0):
			frequencia_dia = "Segunda"
		elif (frequencia == 1):
			frequencia_dia = "Terça";
		elif (frequencia == 2):
			frequencia_dia = "Quarta";
		elif (frequencia == 3):
			frequencia_dia = "Quinta";
		elif (frequencia == 4):
			frequencia_dia = "Sexta";
		elif (frequencia == 5):
			frequencia_dia = "Sábado";
		elif (frequencia == 6):
			frequencia_dia = "Domingo";	
		
		context['data_inicial'] = data_inicial.strftime('%d/%m/%Y')
		context['data_final'] = data_final.strftime('%d/%m/%Y')
		context['frequencia'] = frequencia_dia
		context['membro_selecionado'] = membro_selecionado.nome
		context['entradas'] = entradas_formatadas
		context['quantidade_entradas'] = len(set(aux_quantidade))
	
	return render(request, 'core/relatoriomembro.html', context)
	
def cadastrar_entrada(nome, data):
	membro = Membro.objects.filter(nome__iexact=nome)[0]
	
	entrada = Entrada(data=data, membro=membro)
	
	entrada.save()
	

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("kerberus/test/test")
 
def on_message(client, userdata, msg):
    print(msg.topic)
	
    mensagem = msg.payload.decode('utf-8')
    dados = mensagem.split(',')
	
    data = datetime.strptime(dados[1], "%Y-%m-%d %H:%M:%S")
    
    cadastrar_entrada(dados[0], data)
    
    print("Entrada cadastrada")

def simular_comunicacao_mqtt(request):
	client = mqtt.Client()
	client.on_connect = on_connect #callback para conectar no broker mqtt
	client.on_message = on_message #callback chamado ao receber uma mensagem
	 
	client.connect("mqtt.eclipse.org", 1883, 60)
	 
	client.loop_start()
	counter = 0
	
	entradas_simuladas = [
    "GIOVANNI HENRI EMANUEL ARAGAO,2020-10-13 10:00:04", 
    "GIOVANNI HENRI EMANUEL ARAGAO,2020-10-13 10:15:04", 
    "GIOVANNI HENRI EMANUEL ARAGAO,2020-10-13 12:00:04"
    ]
	 
	while (counter < 3):
		time.sleep(2)
		client.publish("kerberus/test/test", entradas_simuladas[counter])
		counter += 1

	return redirect('dashboard')		
