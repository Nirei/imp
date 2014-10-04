# -*- encoding: utf-8 -*-

import requests
import threading
import sys

# pagina
# lista actual de pelis
# user/pass

# Encapsula un thread que lanza la funcion pasada en el constructor.
class RequestThread(threading.Thread):
        
    def __init__(self, handler, method, url, params, data, cookies, *args):
        super(RequestThread, self).__init__()
        self._handler = handler
        self._method = method
        self._url = url
        self._params = params
        self._data = data
        self._cookies = cookies
        self._args = args
        
    def _request_function(self):
        print(self._method)
        print(self._url)
        print(self._params)
        print(self._data)
        print(self._cookies)
        print(self._args)
        try:
            response = requests.request(self._method, self._url, params=self._params, data=self._data, cookies=self._cookies)
            self._handler(response, self._args)
        except:
            print(self._method)
            print(self._url)
            print(self._params)
            print(self._data)
            print(self._cookies)
            print(self._args)
            e = sys.exc_info()[1]
            self._args[0].login_answer(False, 'Error del servidor:\n' + str(e))
    
    def run(self):
        self._request_function()
    

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
            
    def _login_request(self, r, args):                
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
            args[0].login_answer(False, 'Usuario o contraseña incorrectas')
        # Server refused to answer us (404, 500...)
        else:
            args[0].login_answer(False, 'El servidor no se encuentra disponible')

    def _logout_request(self, r, args):
        # Server answered and we are logged out
        if self._request_successful(r):
            self._login = None
            self._cookie_jar = None
            args[0].logout_answer(True, '')
        # Server answered but somehow he couldn't logged us out
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            args[0].logout_answer(False, 'No se pudo desasociar del sistema')
        # Server refused to answer us (404, not responding...)
        else:
            args[0].logout_answer(False, 'El servidor no se encuentra disponible')
            
    def _page_request(self, r, args):
        url_next = self._server_url + '/movies/page/' + str(args[1]+1)
            
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
            raise Exception()
    
    def _movie_request(self, r, args):
        if self._request_successful(r):
            args[0].movie_request_answer(r.json()['data'])
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            print(r)
            print(r.json())
        else:
            raise Exception()
    
    def _add_request(self, r, args):
        if self._request_successful(r):
            args[0].add_request_answer(True)
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            print(r)
            print(r.json())
        else:
            raise Exception()
        
    ### MODEL FUNCTIONS ###
    
    def get_username(self):
        return self._login
    
    def prev_page(self):
        self._page_number-=1
    
    def next_page(self):
        self._page_number+=1
    
    # Feature: access control
    def login(self, controller, user, passwd):
        #We are trying to connect with a user we have already logged, do nothing
        if user == self._login:
            controller.login_answer(False, 'El usuario ya está conectado')
        else:
            url = self._server_url + '/login'
            data = {'username' : user, 'passwd' : passwd}
            rt = RequestThread(self._login_request, 'POST', url, None, data, self._cookie_jar, controller, user, passwd)
            rt.start()
    
    def logout(self, controller):
        url = self._server_url + '/logout'
        rt = RequestThread(self._logout_request, 'GET', url, None, None, self._cookie_jar, controller)
        rt.start()
    
    # Feature: movie list
    def get_list(self, controller):
        url = self._server_url + '/movies/page/' + str(self._page_number)
        rt = RequestThread(self._page_request, 'GET', url, None, None, self._cookie_jar, controller, self._page_number)
        rt.start()
    
    def get_movie(self, controller, number):
        m_id = self._page[number]['id']
        url = self._server_url + '/movies/' + str(m_id)
        rt = RequestThread(self._movie_request, 'GET', url, None, None, self._cookie_jar, controller, m_id)
        rt.start()
    
    def add_movie(self, controller, movie):
        url = self._server_url + '/movies'
        data = movie
        rt = RequestThread(self._add_request, 'POST', url, None, data, self._cookie_jar, controller, movie)
        rt.start()
    
    def del_movie(self, *args):
        pass
    
    def modify_movie(self, *args):
        pass
    
    def is_logged_in(self):
        return self._login # None == False
    
