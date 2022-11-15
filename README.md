# Amigo Secreto - TCC

## Requirements

- [Python 3.9](https://www.python.org)
- [Docker Compose](https://docs.docker.com/compose/)
- [Virtualenv](https://github.com/pypa/virtualenv/)
- [Git](https://git-scm.com/)
- [Node 19.0](https://nodejs.org/en/download/)

## Rodar o projeto.
- Faça o download para uma pasta do seu computador: `git clone https://github.com/eduardo-monita/base-python-django.git`

### Passos a passo para rodar o proejto.
- Atualizar o pip: `python3.9 -m pip install --upgrade pip`;
- Instalar a virtualenv: `python3.9 -m pip virtualenv`;
- Criar a virtualenv: `python3.9 -m virtualenv venv`;
- Criá-la na pasta raiz do projeto: `venv/Scripts/activate`;
- Instalar os pacotes necessários: `pip install -r requirements.txt`;
- Para inicializar o banco de dados rode: `docker-compose up -d`;
- Baixar pacotes do node: `npm install`;
- Baixar todos os arquivos estáticos do manager do django: `python manage.py collectstatic`;
- Criar as tabelas da Django: `python manage.py migrate`;
- Criar um usuário no seu admin: `python manage.py createsuperuser`;
- Rodar o servidor: `python manage.py runserver`;
- Acessar no browser: `http://localhost:8000/admin`.

## Trabalhando com o gulp
https://gulpjs.com/docs/en/getting-started/quick-start/

## Caso precise baixar o drive do chrome novamente é preciso rodar o seguinte código
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

Link referencia selenium: https://dev.to/mdrhmn/web-scraping-using-django-and-selenium-3ecg
https://github.com/mdrhmn/dj-selenium