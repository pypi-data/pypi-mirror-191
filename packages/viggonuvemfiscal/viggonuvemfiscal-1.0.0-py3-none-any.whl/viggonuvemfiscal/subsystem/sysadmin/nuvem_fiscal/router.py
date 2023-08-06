from viggocore.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)
        self.collection_url = 'nuvem_fiscals'
        self.resource_url = 'nuvem_fiscal'

    @property
    def routes(self):
        return [
            {
                'action': 'Cadastrar empresa na Nuvem Fiscal',
                'method': 'POST',
                'url': self.collection_url + '/cadastrar_empresa',
                'callback': 'cadastrar_empresa',
                'bypass': True
            },
        ]
