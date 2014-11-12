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


#    # Login request
#    def login_request(self, r, args):
#        # Server answered and we are logged
#        if self.is_logged_in(r):
#            self._cookie_jar = r.cookies
#            self._login = args[1]
#            # We have to delete the TextEntry used!
#            args[0]._builder.get_object("user-entry").set_text('')
#            args[0]._builder.get_object("passwd-entry").set_text('')
#            args[0].login_answer(True, '')
#        # Server answered but the user or their passwd are incorrect
#        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
#            args[0].login_answer(False, _(u"Invalid login or password"))
#        # Server refused to answer us (404, 500...)
#        else:
#            args[0].login_answer(False, _(u"Server is not reachable"))
#
#    # Logout request
#    def logout_request(self, r, args):
#        # Server answered and we are logged out
#        if self._request_successful(r):
#            self._login = None
#            self._cookie_jar = None
#            self._page_number = 1
#            args[0].logout_answer(True, '')
#        # Server answered but somehow he couldn't logged us out
#        elif r.status_code == requests.codes.ok and r.json()['result'] == 'failure':
#            args[0].logout_answer(False, _(u"Couldn't logout"))
#        # Server refused to answer us (404, not responding...)
#        else:
#            args[0].logout_answer(False, _(u"Server is not available"))
#
#    # Is already logged
#    def is_logged_in(self):
#        return self._login # None == False


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

	# First we check the fav status of this movie
	check = self.send_request('GET', url, None, cookie)

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

    def send_request(self, method, url, data, cookies):

	response = requests.request(method, url, params=None, data, cookie=cookies)

	# We return the JSON Object received in the response
	return response.json()

	


















    
    
