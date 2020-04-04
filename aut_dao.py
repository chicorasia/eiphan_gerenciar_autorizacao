from model import *

import pyrebase
from firebasedata import LiveData


lista_autorizacoes = []

CONFIG = {
      "apiKey": "AIzaSyAx8Ns1fj_CJ5dwU4RI8jGcJpqD1TOiWT4",
      "authDomain": "iphanautorizacoes.firebaseapp.com",
      "databaseURL": "https://iphanautorizacoes.firebaseio.com",
      "storageBucket": "iphanautorizacoes.appspot.com",
      "serviceAccount": "keys/iphanautorizacoes-firebase-adminsdk-9jmln-bbf264895c.json"
    }

firebase = pyrebase.initialize_app(CONFIG)
db = firebase.database()

def stream_handler(message):
    if message["event"] == 'put' or 'patch':
        print(message["event"])
        atualiza_db()

my_stream = db.child("autorizacao").stream(stream_handler)

def inicializa_db():
    preenche_lista_partir_da_db(db)

def atualiza_db():
    lista_autorizacoes.clear()
    preenche_lista_partir_da_db(db)


def preenche_lista_partir_da_db(db):

    lista_autorizacoes.clear()
    autorizacoes_db = db.child('autorizacao').get()

    for a in autorizacoes_db.each():
        autorizacao = a.val()

        # cria um endereco
        endereco_do_bem_recuperado = Endereco(autorizacao['enderecoDoBem']['logradouro'], autorizacao['enderecoDoBem']['numero'],
                                       autorizacao['enderecoDoBem']['cep'], autorizacao['enderecoDoBem']['cidade'],
                                       autorizacao['enderecoDoBem']['estadoPosicao'],
                                       autorizacao['enderecoDoBem']['complemento'])

        # cria um perfil
        perfil_recuperado = Perfil(autorizacao['perfil']['nome'], autorizacao['perfil']['cpf'],
                                   Endereco(autorizacao['perfil']['endereco']['logradouro'],
                                            autorizacao['perfil']['endereco']['numero'],
                                            autorizacao['perfil']['endereco']['cep'],
                                            autorizacao['perfil']['endereco']['cidade'],
                                            autorizacao['perfil']['endereco']['estado'],
                                            autorizacao['perfil']['endereco']['complemento']), autorizacao['perfil']['email'],
                                   autorizacao['perfil']['telefone'], autorizacao['perfil']['uid'], autorizacao['perfil']['keyPerfil'])

        # cria uma autorizacao, usando o endereço e o perfil recém-criados
        aut_recuperada = Autorizacao(autorizacao['numeroProcesso'], autorizacao['dataProtocolo'], autorizacao['keyAutorizacao'], autorizacao['keyPerfil'],
                                     autorizacao['tipoComoString'], autorizacao['uid'], autorizacao['dataEnvio'],
                                     perfil_recuperado, endereco_do_bem_recuperado, autorizacao['descricao'],
                                     autorizacao['autorizado'], autorizacao['dataResposta'], 'complementares')

        #adiciona a autorização à lista
        lista_autorizacoes.append(aut_recuperada)
        lista_autorizacoes.reverse()


def conta_aguardando_protocolo():
    contagem_aguardando = []
    for a in lista_autorizacoes:
        if a.numero_processo == 'Aguardando protocolo':
            contagem_aguardando.append(a)
    return len(contagem_aguardando)

def contagem():
    return len(lista_autorizacoes)

def recupera_um_processo(posicao):
    aut_recuperada = lista_autorizacoes.get(posicao)
    print(aut_recuperada)

def get_aut_por_key(key_autorizacao):
    return lista_autorizacoes[key_autorizacao]

def grava_data_de_protocolo(key_autorizacao, data_protocolo, numero_processo):

    db.child("autorizacao").child(key_autorizacao).update({"dataProtocolo": data_protocolo})
    db.child("autorizacao").child(key_autorizacao).update({"numeroProcesso" : numero_processo})

def grava_status_do_processo(key_autorizacao, autorizado, data_resposta):
    db.child("autorizacao").child(key_autorizacao).update({"autorizado": autorizado})
    db.child("autorizacao").child(key_autorizacao).update({"dataResposta": data_resposta})





