# ACCESO A LA API (CONCURRENTE)
import requests

# pagina
# lista actual de pelis
# user/pass

class Model:

    def __init__(self, server_url):
        self._server_url = server_url
    
    # Feature: access control
    def login(self, view, user, passwd):
        view.login_answer(False, "dummy method")
    
    def logout(self, view):
        return false, "dummy method"
    
    # Feature: movie list
    def get_list(self, *args):
        return false, "dummy method"
    
    def add_movie(self, *args):
        return false, "dummy method"
    
    def del_movie(self, *args):
        return false, "dummy method"
    
    def modify_movie(self, *args):
        return false, "dummy method"
