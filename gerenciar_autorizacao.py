from flask import Flask, render_template, request, jsonify, url_for, redirect
from datetime import datetime
from model import data_como_string

app = Flask(__name__)

import aut_dao

dao = aut_dao.lista_autorizacoes
aut_dao.inicializa_db()

def data_como_timestamp():
    now = datetime.now()
    data_como_timestamp = int(datetime.timestamp(now)*1000)
    return data_como_timestamp

@app.route('/index')
def index():
    aut_dao.atualiza_db()
    return render_template('index.html', titulo="Gerenciador de Processos do E•Iphan!", autorizacoes=dao,
                           contagem=aut_dao.contagem(), aguardando=aut_dao.conta_aguardando_protocolo())

@app.route('/informar_numero_processo', methods=['GET',])
def informar_numero_processo():
    key_autorizacao = request.args.get('key_autorizacao')
    for autorizacao in dao:
        if autorizacao.key_autorizacao == key_autorizacao:
            return render_template('informar_numero_processo.html', autorizacao=autorizacao)

@app.route('/definir_numero_processo', methods=['GET',])
def definir_numero_processo():
    key_autorizacao = request.args.get('key_autorizacao')
    numero_processo = request.args.get('numero_processo')
    data_protocolo = data_como_timestamp()
    for autorizacao in dao:
        if autorizacao.key_autorizacao == key_autorizacao:
           aut_dao.grava_data_de_protocolo(key_autorizacao, data_protocolo, numero_processo)
           return render_template('definir_numero_processo.html', autorizacao=autorizacao,
                                  numero_processo=numero_processo, data_protocolo=data_como_string(data_protocolo))
        # return redirect(url_for('index'))

@app.route('/login')
def autenticar():
    return '<h1> Página de login com autenticação do google </h1>'
    # return render_template('login.html', titulo="Página de login com autenticação do google")

@app.route('/visualizar', methods=['GET',])
def visualizar():
    key_autorizacao = request.args.get('key_autorizacao')
    for autorizacao in dao:
        if autorizacao.key_autorizacao == key_autorizacao:
            # autorizacao.data_validade = autorizacao.calcula_validade_autorizacao()
            # status=autorizacao.status_do_pedido
            return render_template('visualizar.html', autorizacao=autorizacao)

@app.route('/responder', methods=['GET',])
def responder():
    key_autorizacao = request.args.get('key_autorizacao')
    for autorizacao in dao:
        if autorizacao.key_autorizacao == key_autorizacao:
            return render_template('responder.html', autorizacao=autorizacao)

@app.route('/definir_resposta', methods=['GET',])
def definir_resposta():
    key_autorizacao = request.args.get('key_autorizacao')
    autorizado = request.args.get('autorizado')
    if autorizado == "False":
        autorizado=False
    elif autorizado == "True":
        autorizado=True
    data_resposta = data_como_timestamp()
    for autorizacao in dao:
        if autorizacao.key_autorizacao == key_autorizacao:
           aut_dao.grava_status_do_processo(key_autorizacao, autorizado, data_resposta)
    return redirect('/index')

app.run(debug=True)

