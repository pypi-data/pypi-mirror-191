import flask

from viggocore.common import exception, utils
from vex.subsystem.commom import controller


class Controller(controller.CommomController):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    def cadastrar_empresa(self):
        data = flask.request.get_json()

        try:
            if data:
                entity = self.manager.cadastrar_empresa(**data)
            else:
                entity = self.manager.cadastrar_empresa()
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        includes = {"itens": {"prod_dis": {}}}
        response = {self.resource_wrap: entity.to_dict(includes)}

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype="application/json")
