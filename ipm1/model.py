# ACCESO A LA API (CONCURRENTE)
import requests

# pagina
# lista actual de pelis
# user/pass

class Model:

    def __init__(self, server_url):
        self._server_url = server_url
        
    def login(self, user, passwd):
        return (false,"dummy method")
