# ACCESO A LA API (CONCURRENTE)
import requests
import threading

# pagina
# lista actual de pelis
# user/pass

# Encapsula un thread que lanza la funcion pasada en el constructor.
class RequestThread(threading.Thread):
        
    def __init__(self, req_fun, *args):
        super(RequestThread, self).__init__()
        self._req_fun = req_fun
        self._args = args
    
    def run(self):
        self._req_fun(self._args)
    

class Model:

    def __init__(self, server_url):
        self._server_url = server_url
        
    ### REQUEST FUNCTIONS ###
        
    def _login_request(self, args):
        print(args)
        args[0].login_answer(False, "dummy method")
    
    ### MODEL FUNCTIONS ###
    
    # Feature: access control
    def login(self, controller, user, passwd):
        rt = RequestThread(self._login_request, controller, user, passwd)
        rt.start()
    
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
