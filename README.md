## Instruções para levantar este projeto na máquina local

### Requisitos
- [Pyhton 3](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)

### 1. Criar ambiente virtual
Recomenda-se que se crie um ambiente virtual separado para o projeto. A série de extensões [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) pode ajudar no gerenciamento desses ambientes.

### 2. Instalar dependências
Depois de ativar seu ambiente virtual, instale as dependências do projeto usando
```
$ pip install -r requirements.txt
```
### 3. Criar arquivo .env

Na raiz do projeto, crie o arquivo .env usando o seguinte comando

```
$ touch .env
```
Utilizando o arquivo `.env_exemplo` como base substitua as informações no arquivo `.env`. Ao chegar neste passo você já deverá ter criado uma base de dados _PostgreSQL_ para o o seu projeto.

```
SECRET_KEY=
DEBUG=
DB_NAME=<db_name>
DB_USER=<db_user>
DB_PASSWORD=<db_password>
DB_HOST=127.0.0.1
```
### 3. Levantar o servidor

Para levantar o servidor execute
```
$ python manage.py runserver
```
Acesse `localhost:8000` no browser e cheque se o projeto está no ar.

### 4. Migrar dados para o banco

Depois de levantado, interrompa o servidor com `Ctrl+C` e execute
```
$ python manage.py migrate
```
Pronto! A configuração do seu ambiente local está completa. Para levantar o servidor novamente repita o Passo 3.
