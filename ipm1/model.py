# -*- encoding: utf-8 -*-

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
        self._login = None
        self._cookie_jar = None
        
        self._page = None
        self._page_number = 1
            
    ### REQUEST FUNCTIONS ###
    
    def _request_successful(self, r):
        return r.status_code == requests.codes.ok and r.json()['result'] == 'success'
            
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
                if self._request_successful(r):
                    self._cookie_jar = r.cookies
                    self._login = args[1]
                    # We have to delete the TextEntry used!
                    args[0]._builder.get_object("user-entry").set_text('')
                    args[0]._builder.get_object("passwd-entry").set_text('')
                    args[0].login_answer(True, '')
                # Server answered but the user or their passwd are incorrect
                elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                    args[0].login_answer(False, 'La contraseña o usuario son incorrectas')
                # Server refused to answer us (404, not responding...)
                else:
                    args[0].login_answer(False, 'El servidor no se encuentra disponible')
            
            except: # There was an exception like connection refused
                e = sys.exc_info()[1]
                args[0].login_answer(False, 'Error del servidor:\n' + str(e))

    def _logout_request(self, args):
        #We have to logout explicitly from the server
        url = self._server_url + '/logout'
        
        try:
            r = requests.get(url, cookies=self._cookie_jar)
            
            # Server answered and we are logged out
            if self._request_successful(r):
                self._login = None
                self._cookie_jar = None
                args[0].logout_answer(True, '')
            # Server answered but somehow he couldn't logged us out
            elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                args[0].logout_answer(False, 'No se pudo desconectar de la base de datos')
            # Server refused to answer us (404, not responding...)
            else:
                args[0].logout_answer(False, 'El servidor no se encuentra disponible')
            
        except: # There was an exception like connection refused
            print(sys.exc_info()[1])
            #e = sys.exc_info()[1]
            #args[0].login_answer(False, 'Error del servidor:\n' + str(e))
    
    def _movie_request(self, args):
        url = self._server_url + '/movies/' + str(args[1])
        
        try:
            r = requests.get(url, cookies=self._cookie_jar)
            if self._request_successful(r):
                args[0].movie_request_answer(r.json()['data'])
            elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                print(r)
                print(r.json())
            else:
                print(r)
        except:
            print(sys.exc_info()[1])
            
    def _page_request(self, args):
        url = self._server_url + '/movies/page/' + str(args[1])
        url_next = self._server_url + '/movies/page/' + str(args[1]+1)
        
        try:
            r = requests.get(url, cookies=self._cookie_jar)
            
            if self._request_successful(r):
                self._page = r.json()['data']
                self._page_number = args[1]
                is_first = self._page_number == 1
                is_last = requests.get(url_next, cookies=self._cookie_jar).json()['result'] == 'failure'
                args[0].page_request_answer(args[1], self._page, is_first, is_last)
            elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
                print(r)
                print(r.json())
            else:
                print(r)
        except:
            #e = sys.exc_info()[1]
            #args[0].login_answer(False, 'Error del servidor:\n' + str(e))
            print(sys.exc_info()[1])
    
    ### MODEL FUNCTIONS ###
    
    # Feature: access control
    def login(self, controller, user, passwd):
        rt = RequestThread(self._login_request, controller, user, passwd)
        rt.start()
    
    def logout(self, controller):
        rt = RequestThread(self._logout_request, controller)
        rt.start()
    
    # Feature: movie list
    def get_list(self, controller):
        rt = RequestThread(self._page_request, controller, self._page_number)
        rt.start()
        
    def next_page(self):
        self._page_number-=1
    
    def prev_page(self):
        self._page_number+=1
    
    def get_movie(self, controller, number):
        rt = RequestThread(self._movie_request, controller, self._page[number]['id'])
        rt.start()
    
    def add_movie(self, *args):
        pass
    
    def del_movie(self, *args):
        pass
    
    def modify_movie(self, *args):
        pass
    
    def is_logged_in(self):
        return self._login # None == False
    
