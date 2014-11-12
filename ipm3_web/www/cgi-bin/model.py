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

    def do_login(params):
        auth = Auth()
        response = auth.login(params)
        if response:
            new_cookie = create_cookie(auth.get_cookie())
            return response, new_cookie
        else:
            return "{'error': 'connection error'}", None

    def do_session(cookie_string):
        auth = Auth()
        response = auth.session(cookie_string)
        if response:
            return response
        else:
            return "{'error': 'connection error'}"

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
            if action == "login": # login returns a new cookie
                response, cookie = do_login(params)
                return response, cookie
            else: # other actions reuse the received cookie
                if cookie_string and cookie_string.startswith("ipm-mdb="):
                    if action == "session":
                        response = do_session(cookie_string[8:])
                    else:
                        response = "{'error': 'incorrect params'}"
                else:
                    response = "{'error': 'incorrect cookie'}"
            return response, None
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
