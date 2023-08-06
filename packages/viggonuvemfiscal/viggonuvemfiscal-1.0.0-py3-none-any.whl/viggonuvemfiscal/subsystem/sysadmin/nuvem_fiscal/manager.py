import flask
import requests
from math import trunc
from viggocore.common import exception
from viggocore.common.subsystem import manager, operation
from viggonuvemfiscal.subsystem.sysadmin.ibge_sync.resource import MessageType


class CadastrarEmpresa(operation.Create):

    def pre(self, **kwargs):
        self.token = self.manager.api.tokens().get(
            id=flask.request.headers.get('token'))

        url = self.manager.BASE_URL_HOMO
        resource = '/empresas'
        self.response = requests.get(url + resource)

        if self.response.status_code != 200:
            raise exception.OperationBadRequest()

        # regioes = self.manager.api.regioes().list()

        # if regioes:
        #     raise exception.OperationBadRequest()

        return self.token is not None and super().pre(**kwargs)

    def do(self, session, **kwargs):
        self.entity.created_by = self.token.user_id
        self.entity = super().do(session, **kwargs)
        return self.entity


class Manager(manager.Manager):
    # BASE_URL_PROD = 'https://api.nuvemfiscal.com.br'
    BASE_URL_HOMO = 'https://api.sandbox.nuvemfiscal.com.br'

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.cadastrar_empresa = CadastrarEmpresa(self)
