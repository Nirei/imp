# -*- encoding: utf-8 -*-

import requests
import sys

#SERVER = "http://localhost:5000"
SERVER = "http://ipm-movie-database.herokuapp.com"

# The classes that handles with the connections to the database server mdb
class Model:
    
    #########################
    ### REQUEST FUNCTIONS ###
    #########################


		### Authentication-related methods ###


    # Login request
    def login_request(self, r, args):
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
            args[0].login_answer(False, _(u"Invalid login or password"))
        # Server refused to answer us (404, 500...)
        else:
            args[0].login_answer(False, _(u"Server is not reachable"))

    # Logout request
    def logout_request(self, r, args):
        # Server answered and we are logged out
        if self._request_successful(r):
            self._login = None
            self._cookie_jar = None
            self._page_number = 1
            args[0].logout_answer(True, '')
        # Server answered but somehow he couldn't logged us out
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            args[0].logout_answer(False, _(u"Couldn't logout"))
        # Server refused to answer us (404, not responding...)
        else:
            args[0].logout_answer(False, _(u"Server is not available"))

    # Is already logged
    def is_logged_in(self):
        return self._login # None == False


		### Movie data-related methods ###

    # Movie page list request    
    def page_request(self, r, args):
        url_next = self._server_url + '/movies/page/' + str(args[1]+1)
            
        if self._request_successful(r):
            self._page = r.json()['data']
            self._page_number = args[1]
            is_first = self._page_number == 1
            is_last = requests.get(url_next, cookies=self._cookie_jar).json()['result'] == 'failure'
            args[0].page_request_answer(True, args[1], self._page, is_first, is_last)
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            args[0].page_request_answer(False, _(u"Couldn't get the page.\nServer response:\n") + r.json()['reason'])
        else:
            raise Exception()

    # Movie data request    
    def _movie_request(self, r, args):
        if self._request_successful(r):
            args[0].movie_request_answer(True, r.json()['data'])
        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
            args[0].movie_request_answer(False, _(u"Couldn't get movie info.\nServer response:\n") + r.json()['reason'])
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
            controller.login_answer(False, _(u"You are already logged"))
        else:
            url = self._server_url + '/login'
            data = {'username' : user, 'passwd' : passwd}
            rt = RequestThread(self._login_request, 'POST', url, None, data, self._cookie_jar, controller, user, passwd)
            rt.start()
    
    def logout(self, controller):
        if self.is_logged_in():
            url = self._server_url + '/logout'
            rt = RequestThread(self._logout_request, 'GET', url, None, None, self._cookie_jar, controller)
            rt.start()
        else:
            controller.logout_answer(False, _(u"You haven't logged yet"))
    
    # Feature: movie list
    def get_list(self, controller):
        if self.is_logged_in():
            url = self._server_url + '/movies/page/' + str(self._page_number)
            rt = RequestThread(self._page_request, 'GET', url, None, None, self._cookie_jar, controller, self._page_number)
            rt.start()
        else:
            controller.page_request_answer(False, _(u"You haven't logged yet"))
    
    def get_movie(self, controller, row):
        if self.is_logged_in():
            m_id = self._page[row]['id']
            url = self._server_url + '/movies/' + str(m_id)
            rt = RequestThread(self._movie_request, 'GET', url, None, None, self._cookie_jar, controller, m_id)
            rt.start()
        else:
            controller.movie_request_answer(False, _(u"You haven't logged yet"))
    
    def add_movie(self, controller, movie):

        # Validate data
        if not self._movie_is_valid(movie):
            controller.add_request_answer(False, _(u"Data introduced not valid"))
            return

        # Require login            
        if self.is_logged_in():
            url = self._server_url + '/movies'
            data = movie
            rt = RequestThread(self._add_request, 'POST', url, None, data, self._cookie_jar, controller)
            rt.start()
        else:
            controller.add_request_answer(False, _(u"You haven't logged yet"))
        
    def modify_movie(self, controller, row, movie):

        # Validate data
        if not self._movie_is_valid(movie):
            controller.modify_request_answer(False, _(u"Data introduced not valid"))
            return

        # Require login
        if self.is_logged_in():
            m_id = self._page[row]['id']
            url = self._server_url + '/movies/' + str(m_id)
            data = movie
            rt = RequestThread(self._modify_request, 'PUT', url, None, data, self._cookie_jar, controller)
            rt.start()
        else:
            controller.modify_request_answer(False, _(u"You haven't logged yet"))
    
    def delete_movie(self, controller, row):
        # Require login
        if self.is_logged_in():
            m_id = self._page[row]['id']
            url = self._server_url + '/movies/' + str(m_id)
            rt = RequestThread(self._delete_request, 'DELETE', url, None, None, self._cookie_jar, controller)
            rt.start()
        else:
            controller.modify_request_answer(False, _(u"You haven't logged yet"))
    

    
    
