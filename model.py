from datetime import datetime, timedelta


def data_como_string(data_em_millis):
    data_em_segundos = data_em_millis / 1000
    return datetime.fromtimestamp(data_em_segundos).strftime('%d/%m/%Y %H:%M:%S')

STATUS_DICT = {'False, False, False': 'Aguardando protocolo',
               'True, False, False': 'Em Análise',
               'True, True, False': 'Não autorizado',
               'True, True, True': 'Autorizado'}

VALIDADE_DICT = {'Informação básica' : '--',
                 'Reforma Simplificada' : '1 ano',
                 'Equipamento publicitário ou sinalização' : '1 ano',
                 'Instalações provisórias' : "1 ano",
                 'Reforma, demolição ou construção nova' : '2 anos',
                 'Restauração' : '2 anos',
                 'Consulta prévia' : '6 meses'}


class Perfil:
    def __init__(self, nome, cpf, endereco, email, telefone, uid, key_perfil):
        self.__nome = nome
        self.__cpf = cpf
        self.endereco = endereco
        self.__email = email
        self.__telefone = telefone
        # proprietario = False
        self.__uid = uid
        self.__key_perfil = key_perfil

    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf

    @property
    def email(self):
        return self.__email

    @property
    def telefone(self):
        return self.__telefone

    @property
    def uid(self):
        return self.__uid

    @property
    def key_perfil(self):
        return self.__key_perfil

    @property
    def endereco_formatado(self):
        return f'{self.endereco.logradouro} {self.endereco.numero} ' \
               f'{self.endereco.complemento}- {self.endereco.cidade} / ' \
               f'{self.endereco.estado} - CEP {self.endereco.cep}'


class Endereco:
    def __init__(self, logradouro, numero, cep, cidade, estado, complemento=''):
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        self.cidade = cidade
        self.estado = estado

    def __str__(self):
        return f'{self.logradouro} {self.numero} {self.complemento}, {self.cidade} - {self.estado}, CEP {self.cep}'


class Usuario:
    def __init__(self):
        pass


class Processo:
    def __init__(self, numero_processo, data_envio, data_protocolo, data_resposta):
        self.__numero_processo = numero_processo
        self.__data_envio = data_envio
        self._data_protocolo = data_protocolo
        self._data_resposta = data_resposta

    def atribui_numero_processo(self, numero_processo):
        self.__numero_processo = numero_processo

    @property
    def numero_processo(self):
        return self.__numero_processo

    @property
    def data_envio(self):
        return data_como_string(self.__data_envio)

    @property
    def data_protocolo(self):
        # return data_como_string(self.__data_protocolo)
        if self._data_protocolo is not -1 or None:
            return data_como_string(self._data_protocolo)
        else:
            return 'Aguardando protocolo'

    @data_protocolo.setter
    def define_data_protocolo(self):
        now = datetime.datetime.now()
        self._data_protocolo = int((datetime.timestamp(now)) * 1000)

    @property
    def data_resposta(self):

        if self._data_resposta is not -1 or None:
            return data_como_string(self._data_resposta)
        else:
            return '--'

    def __str__(self):
        return self.__numero_processo


class Autorizacao(Processo):
    def __init__(self, numero_processo, data_protocolo, key_autorizacao, key_perfil, tipo_como_string, uid, data_envio,
                 perfil,
                 endereco_do_bem, descricao, autorizado, data_resposta, complementares, assinatura=''):
        super().__init__(numero_processo, data_envio, data_protocolo, data_resposta)
        self.__key_autorizacao = key_autorizacao
        self.__key_perfil = key_perfil
        self.tipo_como_string = tipo_como_string
        self.__uid = uid
        self.__perfil = perfil
        self.__endereco_correspondencia = perfil.endereco
        self.__endereco_do_bem = endereco_do_bem
        # TODO: implementar a geolocalização
        # latLng = (lat, lng)
        self.descricao = descricao
        self.complementares = complementares
        self.assinatura = assinatura
        self.autorizado = autorizado
        # arquivosAnexos = []

    @property
    def perfil(self):
        return self.__perfil

    @property
    def key_autorizacao(self):
        return self.__key_autorizacao

    @property
    def uid(self):
        return self.__uid

    def autorizado(self):
        return self.autorizado

    @property
    def endereco_do_bem(self):
        return self.__endereco_do_bem

    @property
    def endereco_formatado(self):
        return f'{self.endereco_do_bem.logradouro} {self.endereco_do_bem.numero} ' \
               f'{self.endereco_do_bem.complemento}- {self.endereco_do_bem.cidade} / ' \
               f'{self.endereco_do_bem.estado} - CEP {self.endereco_do_bem.cep}'

    def data_validade(self, data_validade):
        self.data_validade = data_validade


    def foi_protocolado(self):
        if self._data_protocolo is not -1:
            return 'True'
        else:
            return 'False'

    def foi_respondido(self):
        if self._data_resposta is not -1:
            return 'True'
        else:
            return 'False'

    def foi_autorizado(self):
        if self.autorizado:
            return 'True'
        else:
            return 'False'

    def status_do_pedido(self):

        string_para_dict = self.foi_protocolado() + ", " + self.foi_respondido() + ", " + self.foi_autorizado()
        return STATUS_DICT[string_para_dict]

    def validade(self):

        if self.autorizado is True:
            return VALIDADE_DICT[self.tipo_como_string]
        else :
            return '--'
