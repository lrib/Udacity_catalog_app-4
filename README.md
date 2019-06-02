Construindo um catálogo de itens
=================================


Udacity - Desenvolvedor Web Full-Stack Nanodegree Program
---------------------------------------------
Project 4: Construindo um catálogo de itens

Este projeto tem como a construção de uma aplicação que gera uma lista de itens em várias categorias e um sistema de registro e autenticação de usuários. Aqueles registrados poderão postar, editar e excluir seus próprios itens.
Para a execucao deste projeto as categorias foram baseadas em times de futebol do Rio de janeiro, como Flamengo, Vasco, Botafogo, Fluminense, America e Bangu e os itens são apresentados como os seus jogadores.

Pre-requisitos
------------

+ [Python 2.7.12](https://www.python.org/downloads/release/python-2712/) instalado.
+ A versao pode ser verificada executando o comando abaixo:
```bash
$ python -V
```
+ [Virtual Box](https://www.virtualbox.org/wiki/Downloads) instalado.
+ [Vagrant](https://www.vagrantup.com/downloads.html) instalado.
+ [Arquivos de cofiguracao da VM](https://github.com/udacity/fullstack-nanodegree-vm).
+ [Instalar a lib Python flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask).
+ [Instalar a lib Python sqlalchemy](https://pypi.org/project/SQLAlchemy/).
+ [Instalar a lib Python oauth2client](https://pypi.org/project/oauth2client/).
+ [Instalar a lib Python Google OAuth2 API Client](https://developers.google.com/api-client-library/python/apis/oauth2/v1).
+ [Credenciais Google OAuth 2.0 ](https://console.developers.google.com/apis/credentials).
+ A lista completa de todas as bibliotecas pode ser encontrada no arquivo [requirements.txt](https://github.com/lrib/Udacity_catalog_app-4/blob/master/requirements.txt).
Obs. A chave da credencial deve ser armazenada dentro do arquivo client_secrets.json, detalhado abaixo. 

Uso
-----
* Instalar o Virtual Box e depois o Vagrant, se já não estiver instalada.
* Baixar os [Arquivos de configuração da VM](https://github.com/udacity/fullstack-nanodegree-vm).
* Decompactar o arquivo fullstack-nanodegree-vm-master.zip.
* Dentro do Shell ir para a pasta FSND-Virtual-Machine/vagrant/.
```bash
$ cd FSND-Virtual-Machine/vagrant/
```
* Inicialize a VM (depo demorar um pouco, principalmente se for a primeira vez, pois vai baixo e instalar o Ubuntu Linux.
```bash
$ vagrant up
```
* Faça o ogin an VM.
```bash
$ vagrant ssh
```
* Entre na pasta partilhada /vagrant.
```bash
$ cd /vagrant
```
* Baixe os arquivos da pasta do Git atraves do comando abaixo ou fazendo o downloads para uma pasta especifica
```bash
$ git clone https://github.com/lrib/Udacity_catalog_app-4.git
```
* Verifique se os arquivos abaixo estao na pasta:
	* project.py
	* iniciodb.py
	* database_setup.py
	* client_secrets.json
	* /templates
	* /static

* Entre na pasta abaixo ou em uma outra selecionada 
```bash
$ cd Udacity_catalog_app-4
$ python project.py
```
* Conecte a pagina web atraves do link: http://localhost:5000/
* Na pagina principal é apresentado as Categorias como os Clubes de Futebos e os Itens como os seus Jogadores. 
* Os dados dos Itens podem ser extraidos por JSON, atraves do Link http://localhost:5000/catalog/int:Categoria/categoria.json , onde a Categoria é o nome do time de futebol existente.

Resultado
---------

* Os resultados são apresentados por tipo de acesso.
  + Sem executar o login atravês de uma conta do Google o usuario pode apenas realizar as consultas do Times e Jogadores.
  + Existe a possibilidade do usuario utilizar uma conta do Google para criar, editar e apagar um jogador.
  + Ao executar o login atravês de uma conta do Google o usuario pode criar, editar e apagar um jogador, porem estas ações somente são realizadas pelo usuario que criou o Jogador.
  + A opção de adicionar um novo jogador aparecera assim que o o usuario com login Google selecionar uma Categoria.
  + Existe um acesso a lista dos jogadores por JSON, atravês do [link](http://localhost:5000/catalog/int:Categoria/categoria.json).
  Obs. Substituir o int:Categoria pelo time desejado.
  Um exemplo dos endpoint do JSON é apresentado abaixo:
  
  {"Categoria":
  
   [{
   
    "categoria_id":1,  
    
    "date":"Fri, 31 May 2019 13:58:10 GMT",
    
    "description":"Bruno Henrique Pinto....",
    
    "name":"Bruno Henrique"
    
     }
     
     ....
     
    ]
    
   }

Fontes consultadas
---------
http://pep8online.com/checkresult

http://zetcode.com/python

https://www.w3schools.com

https://developers.google.com/identity/protocols/OAuth2

https://developers.google.com/identity/protocols/OAuth2WebServer

