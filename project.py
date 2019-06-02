from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categoria, Item, User

# New imports
from flask import session as login_session
import random
import string
from os import urandom
from datetime import datetime

# IMPORTS FOR GOOGLE LOGIN
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Import from Google:
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Cliente Web 3"

app = Flask(__name__)

# Start program


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login_google.html', STATE=state)


@app.route('/googleconnect', methods=['POST'])
def googleconnect():
    session.close()
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    token_temp = request.data

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token_temp,
                                              requests.Request(),
                                              CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded toke
        userid = idinfo['sub']

    except ValueError:
        response = make_response(
            json.dumps('Invalid toke.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  # Invalid token
        pass

    # Check that the access token is valid.
    # Details of the response at
    """
    # Check that the access token is valid.
    # Details of the response at
    https://developers.google.com/identity/protocols/OpenIDConnect#obtainuserinfo
    """
    access_token = token_temp
    url = ('https://oauth2.googleapis.com/tokeninfo?id_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = idinfo['sub']

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected. (jSON)'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = token_temp
    login_session['gplus_id'] = gplus_id

    # Get user info
    login_session['username'] = idinfo['name']
    login_session['picture'] = idinfo['picture']
    login_session['email'] = idinfo['email']

    # see if user exists, if it doesn't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
                           border-radius: 150px;\
                           -webkit-border-radius: 150px;\
                           -moz-border-radius: 150px;"> '

    flash("you are now logged in as %s" % login_session['username'])

    return output


@app.route('/logout')
def googlelogout():
    return render_template('logout_google.html')


@app.route('/googledisconnect', methods=['POST'])
def googledisconnect():
    session.close()
    # Disconect from GOOGLE
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps
                                 ('Current user not connected..'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    app.secret_key = urandom(24)

    flash(" Logout do %s realizado com sucesso! " % login_session['username'])

    output = ''
    output += '<h1>Godbay, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
                           border-radius: 150px;\
                           -webkit-border-radius: 150px;\
                           -moz-border-radius: 150px;"> '

    login_session['access_token'] = ""
    login_session['gplus_id'] = ""
    login_session['username'] = ""
    login_session['email'] = ""
    login_session['picture'] = ""

    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    return output

# Show main page (index)


@app.route('/')
def showMenu():
    # Pasta Publica. Todos tem acesso a esta pagina
    # Carrega toda a tabela de Categorias#

    session.close()
    try:
        catalogs = session.query(Categoria).order_by(asc(Categoria.id)) \
                           .limit(7).all()
        # Carrega a tabela com o itens
        items = session.query(Item).order_by(desc(Item.date)).limit(7).all()
        #
    except BaseException:
        session.close()

    if 'username' not in login_session:
        return render_template('index.html', catalogs=catalogs, items=items)
    else:
        return render_template('index_privada.html',
                               catalogs=catalogs,
                               items=items,
                               username=login_session['username'])


# show the Category page (Publico e Privado).

@app.route('/catalog/<string:categoria_name>/')
def showCatalog(categoria_name):
    # Carrega toda a tabela de Categorias#
    session.close()
    catalogs = session.query(Categoria).order_by(asc(Categoria.name)) \
                                       .limit(7).all()
    # Carrega os itens que foi
    try:
        category = session.query(Categoria) \
                          .filter(Categoria.name == categoria_name).one()
        items = session.query(Item).filter(Item.name_cat == category) \
                                   .order_by(desc(Item.date)).limit(5).all()
    except BaseException:
        items = []
    try:
        category = session.query(Categoria) \
                    .filter(Categoria.name == categoria_name).one()

        total_itens = session.query(Item) \
                             .filter(Item.name_cat == category).count()
    except BaseException:
        total_itens = 0

    if 'username' not in login_session:
        return render_template('detalhe_menu.html',
                               categoria_name=categoria_name,
                               items=items,
                               catalogs=catalogs,
                               total_itens=total_itens)

    else:
        return render_template('detalhe_menu_privado.html',
                               categoria_name=categoria_name,
                               items=items, catalogs=catalogs,
                               total_itens=total_itens,
                               username=login_session['username'])


# show the Item page (Publico e Privado).
@app.route('/catalog/<string:categoria_name>/<string:item_name>')
def showItembyCatalog(categoria_name, item_name):
    # Com a categoria e com o item, apresenta a descricao do item;
    session.close()
    try:
        # extrai as informacoes da Categoria e do Item
        category = session.query(Categoria) \
                    .filter(Categoria.name == categoria_name).one()

        subItems = session.query(Item) \
                          .filter(Item.name_cat == category,
                                  Item.name == item_name) \
                          .one()

        # Extrai a descricao do Item
        descricao = subItems.description
        # Extrai o email do criador do Item
        Iduser = session.query(User).filter(User.id == subItems.user_id).one()

        email_utilizador = Iduser.email

    except BaseException:

        descricao = "Descricao nao localizada"

    # Estrutura de decisao:
    # Se esta logado ou nao
    if 'username' not in login_session:
        print ("Publica")
        return render_template('detalhe_item.html',
                               categoria_name=categoria_name,
                               item_name=item_name, descricao=descricao)

    # Se esta logado, se o usuario logado foi quem criou o item
    elif email_utilizador == login_session['email']:
        print ("Privado")
        return render_template('detalhe_item_privado.html',
                               categoria_name=categoria_name,
                               item_name=item_name,
                               descricao=descricao,
                               username=login_session['username'])

    # Se esta logado e se nao e o utilizador q criou o Item
    else:
        print ("Semi-Privado")
        return render_template('detalhe_item_semiprivado.html',
                               categoria_name=categoria_name,
                               item_name=item_name, descricao=descricao,
                               username=login_session['username'])


# show the Item page (Privado) - Edit -.
@app.route('/catalog/<string:categoria_name>/<string:item_name>/Edit',
           methods=['GET', 'POST'])
def EditItembyCatalog(categoria_name, item_name):
    # verifica se o utilizador esta logado
    session.close()
    if 'username' not in login_session:
        # Se chegou aqui e pq nao esta logado
        return redirect('/login')
        # Se chegou com um POST
    if request.method == 'POST':
        xnow = datetime.now()
        # Aponta para o Item item_name na tabela Item para fazer o update
        category = session.query(Categoria) \
                          .filter(Categoria.name == categoria_name).one()

        subItems = session.query(Item).filter(Item.name_cat == category,
                                              Item.name == item_name).one()

        # Faz a atualizacao dos valores
        subItems.name = request.form['new_nome']
        subItems.description = request.form['new_descricao']
        subItems.date = xnow
        if (request.form['new_cat']) == "":
            new_category = session.query(Categoria) \
                                  .filter(Categoria.name == categoria_name) \
                                  .one()

        else:
            new_category = session.query(Categoria) \
                                  .filter(Categoria.name == (request
                                          .form['new_cat'])).one()

        subItems.categoria_id = new_category.id
        subItems.name_cat = new_category
        session.add(subItems)
        session.commit()
        # retorna ao menu principal

        flash("Jogador %s atualizado com sucesso " % request.form['new_nome'])

        return redirect(url_for('showMenu'))

    else:

        try:
            # Extrai as informacoes da Categoria e do Item
            category = session.query(Categoria) \
                        .filter(Categoria.name == categoria_name).one()

            subItems = session.query(Item).filter(Item.name_cat == category,
                                                  Item.name == item_name).one()
            # Extrai a descricao do Item
            descricao_in = subItems.description
            # Extrai o email do criador do Item
            Iduser = session.query(User).filter(User.id == subItems.user_id) \
                                        .one()
            email_utilizador = Iduser.email
            # Apresentar todas as categorias
            catalogs = session.query(Categoria).order_by(asc(Categoria.name)) \
                                               .all()

        except BaseException:

            descricao_in = "Descricao nao localizada"

        return render_template('editar_item.html',
                               categoria_name=categoria_name,
                               item_name=item_name, descricao_in=descricao_in,
                               username=login_session['username'],
                               catalogs=catalogs)


# show the Item page (Privado) - Remove -.
@app.route('/catalog/<string:categoria_name>/<string:item_name>/Delete',
           methods=['GET', 'POST'])
def DeleteItembyCatalog(categoria_name, item_name):
    # verifica se o utilizador esta logado
    session.close()
    if 'username' not in login_session:
        # Se chegou aqui e pq nao esta logado
        return redirect('/login')
        # Se chegou com um POST
    if request.method == 'POST':
        # Aponta para o Item item_name na tabela Item para fazer o update
        category = session.query(Categoria) \
                    .filter(Categoria.name == categoria_name).one()

        subItems = session.query(Item) \
                          .filter(Item.name_cat == category,
                                  Item.name == item_name).one()

        session.delete(subItems)

        session.commit()

        flash("Jogador %s removido com sucesso " % item_name)

        return redirect(url_for('showMenu'))

    else:
        # Fez um get na pagina de Delete
        return render_template("delete_item.html",
                               categoria_name=categoria_name,
                               item_name=item_name)


@app.route('/catalog/<string:categoria_name>/add', methods=['GET', 'POST'])
def addItembyCatalog(categoria_name):
    # verifica se o utilizador esta logado
    session.close()
    if 'username' not in login_session:
        # Se chegou aqui e pq nao esta logado
        return redirect('/login')
        # Se chegou com um POST
    if request.method == 'POST':
        xnow = datetime.now()
        # Extrai a DB Categoria
        catalogs = session.query(Categoria) \
                          .filter(Categoria.name == categoria_name).one()
        # Exteri a DB Usuario
        users = session.query(User) \
                       .filter(User.id == login_session['user_id']).one()
        # Faz a gravacao
        newItem = Item(name=request.form['nome'],
                       description=request.form['descricao'],
                       user_id=login_session['user_id'],
                       date=xnow,
                       categoria_id=catalogs.id,
                       name_cat=catalogs,
                       user=users)

        session.add(newItem)
        flash('Novo jogador %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('showMenu'))

    else:
        return render_template('adicionar_item.html',
                               categoria_name=categoria_name)


# Making an API Endpoint (GET Request) - All Items IN Item
@app.route('/catalog/<string:categoria_name>/categoria.json')
def restaurantMenuJSON(categoria_name):
    session.close()
    try:
        category = session.query(Categoria) \
                          .filter(Categoria.name == categoria_name).one()
        items = session.query(Item) \
                       .filter(Item.name_cat == category) \
                       .order_by(desc(Item.date)).all()
    except BaseException:
        items = []
    return jsonify(Categoria=[i.serialize for i in items])

# Connect to Database and create database session


engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # app.debug = True
    app.run(host='0.0.0.0', port=5000)
