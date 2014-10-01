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
        url = self._server_url + '/login'
        payload = 'username=' + args[1] + '&passwd=' + args[2]
        
        r = requests.post(url, payload)
        
        if r.status_code == requests.codes.ok and r.json()['result'] == 'success':
            self._id_cookie = r.cookies['rack.session']
            args[0].login_answer(True)
        else:
            print(r)
            print(r.url)
            print(r.text)
            args[0].login_answer(False, r.json()['reason'])
    
    ### MODEL FUNCTIONS ###
    
    # Feature: access control
    def login(self, controller, user, passwd):
        rt = RequestThread(self._login_request, controller, user, passwd)
        rt.start()
    
    def logout(self):
        self._id_cookie = None
    
    # Feature: movie list
    def get_list(self, *args):
        pass
    
    def add_movie(self, *args):
        pass
    
    def del_movie(self, *args):
        pass
    
    def modify_movie(self, *args):
        pass
