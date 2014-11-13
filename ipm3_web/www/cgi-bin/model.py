#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import cgi
import Cookie
import os
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
                new_cookie = self.create_cookie(data.cookies['rack.session'])
                return response, new_cookie
            else:
                return None, None              
        except requests.exceptions.ConnectionError:
            return "{'error': 'connection error'}", None

    # Ask the server if the browser's cookie is still valid
    def session_request(self, cookie):
        url = self.server_url + '/session'
        try:
            data = self.send_request('GET', url, None, cookie)
            return data.text
        except requests.exceptions.ConnectionError:
            return "{'error': 'connection error'}"


    # Do logout
    def logout_request(self, cookie):
        url = self.server_url + '/logout'
        try:
            data = self.send_request('GET', url, None, cookie)
            return data.text
        except requests.exceptions.ConnectionError:
            return "{'error': 'connection error'}"


        ### Movie data-related methods ###

    # Get new movie page
    def movie_page_request(self, params):
        # We assume Javascript already give us the page the browser wants
        url = self.server_url + '/movies/page/' + str(params["page"])
        response = self.send_request('GET', url, None, None)
        return response.text

    # Get movie data
    def movie_request(self, params):
        url = self.server_url + '/movies/' + str(params["movie_id"])
        response = self.send_request('GET', url, None, None)
        return response.text

    # Get fav status
    def fav_request(self, params, cookie):    
        url = self.server_url + '/movies/' + str(params["movie_id"]) + '/fav'
        # First we check the fav status of this movie
        response = self.send_request('GET', url, None, cookie)
        return response.text

    # Change favorite
    def fav_mark_request(self, params, cookie):
        url = self.server_url + '/movies/' + str(params["movie_id"]) + '/fav'
        # We will mark/unmark depending on the current fav status of the movie
        if(str(params["mark"]) == "true"):
            method = 'POST'
        else:
            method = 'DELETE'
        response = self.send_request(method, url, None, cookie)
        return response.text


        ### Comments-related methods ### 

    # Get comments page
    def comments_request(self, params):
        # We assume Javascript already give us the page the browser wants
        url = self.server_url + '/movies/' + str(params["movie_id"]) + '/comments/page/' + str(params["page"])
        response = self.send_request('GET', url, None, None)
        return response.text

    # Post new comment
    def post_comment_request(self, params, cookie):
        url = self.server_url + '/movies/' + str(params["movie_id"]) + '/comments'
        content = dict(content = params["comment"])
        response = self.send_request('POST', url, content, cookie)
        return response.text

    # Delete comment
    def del_comment_request(self, params, cookie):
        url = self.server_url + '/movies/' + str(params["movie_id"]) + '/comments/' + str(params["comment_id"])
        response = self.send_request('DELETE', url, None, cookie)
        return response.text


        ### Private methods ###

    # Send the final request to the server
    def send_request(self, method, url, datos, cookie):
        response = requests.request(method, url, params=None, data=datos, cookies=cookie)
        # We return the response
        return response

    # Parse request params
    def get_params(self):
        form = cgi.FieldStorage()
        action = None
        params = None
        print form
        if form.has_key("action"):
            action = form["action"].value
        # Login
        if form.has_key("username") and form.has_key("passwd"):
            params = dict(username = form["username"].value, passwd = form["passwd"].value)
        # Movie page request
        if form.has_key("page"):
            params = dict(page = form["page"].value)
        if form.has_key("movie_id"):
            # Get comments
            if form.has_key("page"):
                params = dict(movie_id = form["movie_id"].value, page = form["page"].value)
            # Set fav status
            elif form.has_key("mark"):
                params = dict(movie_id = form["movie_id"].value, mark = form["mark"].value)
            # Send comment
            elif form.has_key("comment"):
                params = dict(movie_id = form["movie_id"].value, comment = form["comment"].value)
            # Delete comment
            elif form.has_key("comment_id"):
                params = dict(movie_id = form["movie_id"].value, comment_id = form["comment_id"].value)
            # Movie data request
            # Get fav status
            else:
                params = dict(movie_id = form["movie_id"].value)
        return action, params

    # Creates a new cookie from a string
    def create_cookie(self, cookie_string):
        cookie = None
        if cookie_string:
            cookie = Cookie.SimpleCookie()
            cookie['ipm-mdb'] = cookie_string
            cookie['ipm-mdb']['expires'] = 24 * 60 * 60
        return cookie


        ### Main of cgi script ###

    def main(self, cookie_string):
        action, params = self.get_params()
        if action:
            ##Actions that do not need a cookie##
            if action == "movie_list":
                response = self.movie_page_request(params)
                return response, None
            elif action == "movie_data":
                response = self.movie_request(params)
                return response, None
            elif action == "get_comments":
                response = self.comments_request(params)
                return response, None
            ##Actions that return a cookie##
            elif action == "login":
                response, cookie = self.login_request(params)
                return response, cookie
            ##Actions that need a cookie##
            elif cookie_string and cookie_string.startswith("ipm-mdb="):
                # Creating new cookie jar
                cookie_jar = requests.cookies.cookielib.CookieJar()
                # Creating a new cookie with the string of cookie given by the browser
                cookie_session = requests.cookies.create_cookie('rack.session', cookie_string[8:])
                # Introducing the cookie into the cookie jar
                cookie_jar.set_cookie(cookie_session)
                if action == "logout":
                    response = self.logout_request(cookie_jar)
                elif action == "session":
                    response = self.session_request(cookie_jar)
                elif action == "get_fav":
                    response = self.fav_request(params, cookie_jar)
                elif action == "set_fav":
                    response = self.fav_mark_request(params, cookie_jar)
                elif action == "new_comment":
                    response = self.post_comment_request(params, cookie_jar)
                elif action == "del_comment":
                    response = self.del_comment_request(params, cookie_jar)
                return response, None
            else:
                return "{'error': 'incorrect cookie'}", None

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
