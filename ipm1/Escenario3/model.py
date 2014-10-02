# -*- encoding: utf-8 -*-

# ACCESO A LA API (CONCURRENTE)
import requests
import threading
import sys

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
	self._login = ''
	self._id_cookie = ''
        
    ### REQUEST FUNCTIONS ###
        
    def _login_request(self, args):
        url = self._server_url + '/login'
        payload = 'username=' + args[1] + '&passwd=' + args[2]

	#We are trying to connect with a user we have already logged, do nothing
	if args[1] == self._login:
	    args[0].login_answer(False, 'El usuario ya está conectado')
	else:
            try:
	        r = requests.post(url, payload)

	        # Server answered and we are logged
                if r.status_code == requests.codes.ok and r.json()['result'] == 'success':
                    self._id_cookie = r.cookies['rack.session']
		    self._login = args[1]
		    # We have to delete the TextEntry used!
		    args[0]._builder.get_object("user-entry").set_text('')
		    args[0]._builder.get_object("passwd-entry").set_text('')
                    args[0].login_answer(True, '')
	        # Server answered but the user or their passwd are incorrect
                elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                    args[0].login_answer(False, 'La contraseña o usuario son incorrectas')
	        # Server refused to answer us (404, not responding...)
	        elif r.status_code != requests.codes.ok:
	            args[0].login_answer(False, 'El servidor no se encuentra disponible')

	    except: # There was an exception like connection refused
	        e = sys.exc_info()[1]
	        args[0].login_answer(False, 'Error del servidor:\n' + str(e))

    def _logout_request(self, args):
	#We have to logout explicitly from the server
	url = self._server_url + '/logout'
	cookies = dict(cookies_are=self._id_cookie)

	try:
	    r = requests.get(url, cookies=cookies)

	    # Server answered and we are logged out
            if r.status_code == requests.codes.ok and r.json()['result'] == 'success':
                self._id_cookie = ''
	        self._login = ''
                args[0].logout_answer(True, '')
	    # Server answered but somehow he couldn't logged us out
            elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                args[0].logout_answer(False, 'No se pudo desconectar de la base de datos')
	    # Server refused to answer us (404, not responding...)
	    elif r.status_code != requests.codes.ok:
	        args[0].logout_answer(False, 'El servidor no se encuentra disponible')

	except: # There was an exception like connection refused
	    e = sys.exc_info()[1]
	    args[0].login_answer(False, 'Error del servidor:\n' + str(e))
	
    
    ### MODEL FUNCTIONS ###
    
    # Feature: access control
    def login(self, controller, user, passwd):
        rt = RequestThread(self._login_request, controller, user, passwd)
        rt.start()
    
    def logout(self, controller):
        rt = RequestThread(self._logout_request, controller)
	rt.start()
    
    # Feature: movie list
    def get_list(self, *args):
        pass
    
    def add_movie(self, *args):
        pass
    
    def del_movie(self, *args):
        pass
    
    def modify_movie(self, *args):
        pass
