#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import sys

# The classes that handles with the connections to the database server mdb
class Model:

    ##########################
    ### Private attributes ###
    ##########################

    #server_url = "http://localhost:5000"
    server_url = "http://ipm-movie-database.herokuapp.com"    

    #########################
    ### REQUEST FUNCTIONS ###
    #########################


		### Authentication-related methods ###

    # Do login
    def login_request(self, login_data):
        response = None
        url = self.server_url + '/login'
        try:
            data = self.send_request('POST', url, login_data, None)
            response = data.text
            if response:
                new_cookie = self.create_cookie(data.cookies)
                return response, new_cookie
            else:
                return None, None              
        except requests.exceptions.ConnectionError:
            return "{'error': 'connection error'}", None

    #def session_request(self, cookie_string):
     #   auth = Auth()
      #  response = auth.session(cookie_string)
       # if response:
        #    return response
        #else:
        #    return "{'error': 'connection error'}"

		### Movie data-related methods ###

    # Get new movie page
    def movie_page_request(self, page):
	    # We assume Javascript already give us the page the browser wants
        url = self.server_url + '/movies/page/' + str(page)
    	response = self.send_request('GET', url, None, None)
	    return response

    # Get movie data
    def movie_request(self, movie_id):
	    url = self.server_url + '/movies/' + str(movie_id)
	    response = self.send_request('GET', url, None, None)
	    return response

    # Get fav status
    def fav_request(self, movie_id, cookie):    
	    url = self.server_url + '/movies/' + str(movie_id) + '/fav'
        # First we check the fav status of this movie
	    response = self.send_request('GET', url, None, cookie)
	    return response

    # Change favorite
    def fav_mark_request(self, movie_id, mark, cookie):
        url = self.server_url + '/movies/' + str(movie_id) + '/fav'
	    # We will mark/unmark depending on the current fav status of the movie
	    if(mark):
	        method = 'POST'
	    else:
	        method = 'DELETE'
	    response = self.send_request(method, url, None, cookie)
	    return response

		### Comments-related methods ### 

    # Get comments page
    def comments_request(self, movie_id, page):
	    # We assume Javascript already give us the page the browser wants
	    url = self.server_url + '/movies/' + str(movie_id) + '/comments/page/' + str(page)
	    response = self.send_request('GET', url, None, None)
    	return response

    # Post new comment
    def post_comment_request(self, movie_id, comment, cookie):
        url = self.server_url + '/movies/' + str(movie_id) + '/comments'
    	response = self.send_request('POST', url, comment, cookie)
    	return response

    # Delete comment
    def del_comment_request(self, movie_id, comment_id, cookie):
	    url = self.server_url + '/movies/' + str(movie_id) + '/comments/' + str(comment_id)
    	response = self.send_request('DELETE', url, None, cookie)
    	return response

		### Private methods ###

    # Send the final request to the server
    def send_request(self, method, url, data, cookies):
    	response = requests.request(method, url, params=None, data, cookie=cookies)
        # We return the JSON Object received in the response
        return response.json()

    # Parse request params
    def get_params():
        form = cgi.FieldStorage()
        action = None
        params = None
        if form.has_key("action"):
            action = form["action"].value
        if form.has_key("username") and form.has_key("passwd"):
            params = dict(username=form["username"].value, passwd=form["passwd"].value)
        return action, params

    # Creates a new cookie from a string
    def create_cookie(cookie_string):
        cookie = None
        if cookie_string:
            cookie = Cookie.SimpleCookie()
            cookie['ipm-mdb'] = cookie_string
            cookie['ipm-mdb']['expires'] = 24 * 60 * 60
        return cookie


		### Main of this cgi script ###

    def main(cookie_string):
        action, params = get_params()
        if action:
            ##Actions that do not need a cookie##
            if action == "movie_list":
            elif action == "movie_data":
            elif action == "get_comments":
            ##Actions that return a cookie##
            elif action == "login":
                response, cookie = self.login_request(params)
                return response, cookie
            ##Actions that need a cookie##
            elif cookie_string and cookie_string.startswith("ipm-mdb="):
                cook = cookie_string[8:]
                if action == "logout":
                elif action == "session":
                    response = self.session_request(cook)
                elif action == "set_fav":
                elif action == "new_comment":
                elif action == "del_comment":

                return response, None
            else:
                return response = "{'error': 'incorrect cookie'}"

                
            else: # other actions reuse the received cookie

        return "{'error': 'incorrect url'}", None

try:
    cookie_string = os.environ.get('HTTP_COOKIE') # get the cookie
    modelo = Model()
    response, cookie = modelo.main(cookie_string)
    if cookie:
        print cookie
    print 'Content-Type: application/json\n\n'
    print response
except:
        cgi.print_exception()
