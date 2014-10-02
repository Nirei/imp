# -*- encoding: utf-8 -*-

import threading
from gi.repository import Gtk, GObject
from model import *

class Controller(threading.Thread):

    # UI MANAGEMENT PRIVATE METHODS #

    def _show_window(self, window, boolean):
        window = self._builder.get_object(window)
        if boolean:
            window.show()
        else:
            window.hide()
        
    def _show_main_window(self, boolean):
        self._show_window("main-window", boolean)

    def _show_login_dialog(self, boolean):
        self._show_window("login-dialog", boolean)

    def _show_error(self, message):
        # Solo una instancia activa del mensaje de error en cada momento... Concurrencia?
        # synchronized method de java?
        dialog = self._builder.get_object('error-dialog')
        # Ugly hack to edit dialog message
        dialog.get_children()[0].get_children()[0].get_children()[1].get_children()[1].set_text(message)
        dialog.run()
        
        dialog.hide()
    
    def _update_movie_list():
        self._movie_list.clear()
        self._label_page.set_text(str(self._page_number))
        for movie in self._movie_page:
            self._movie_list.append(movie['title'])

    ### CONSTRUCTOR & INHERITED METHODS ###

    def __init__(self, model):
        super(Controller, self).__init__()
        self._model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file('gui.glade')
        self._builder.connect_signals(self)
        
        self._movie_page = None
        self._page_number = -1
        self._movie_list = self._builder.get_object('movie-list')
        self._label_page = self._builder.get_object('label-page')
        
        self._show_login_dialog(True)
    
    def run(self):
	GObject.threads_init()
        Gtk.main()
    
    ###### HANDLERS!! ######
    
    # Login dialog handlers
    def on_login_dialog_close(self, *args):
        Gtk.main_quit(*args)
    
    def on_dialog_login_button_clicked(self, widget):
        user = self._builder.get_object('user-entry').get_text()
        passwd = self._builder.get_object('passwd-entry').get_text()

        if user == '':
            self._show_error('No ha introducido un nombre de usuario')
        elif passwd == '':
            self._show_error('No ha introducido una contraseña')
        else:
            self._model.login(self, user, passwd)

    # Windows handlers
    def on_exit(self, *args):
        Gtk.main_quit(*args)

    def on_exit_without_logout(self, *args):
	    print("Por implementar")
	    self.on_exit(args)	
    
    # Menu handlers
    
    # Toolbar handlers
    def on_add_movie(self, widget):
        print("on_button_add_clicked")
    
    def on_modify_movie(self, widget):
        print("on_button_modify_clicked")
    
    def on_delete_movie(self, widget):
        print("on_button_delete_clicked")
    
    def on_logout(self, widget):
        self._model.logout(self)
    
    # Content handlers
    def on_selection_changed(self, tso):
        (a,b) = tso.get_selected()
        print(a[b][0])
    
    ###### CALLBACKS!! ######
    # Estas funciones son para llamar desde el modelo, de modo que si realizan
    # cambios en la interfaz deben hacerlo a traves de GObject.idle_add()
    
    def login_answer(self, *args):
	# Success
        if args[0]:
            GObject.idle_add(self._show_login_dialog, False)
            GObject.idle_add(self._show_main_window, True)
	# Failure
        else:
            GObject.idle_add(self._show_error, args[1])

    def logout_answer(self, *args):
	# Success
        if args[0]:
            GObject.idle_add(self._show_main_window, False)
            GObject.idle_add(self._show_login_dialog, True)
	# Failure
        else:
            GObject.idle_add(self._show_error, args[1])

    def page_request_answer(number, page):
        self._page_number = number
        self._movie_page = page
        
        GObject.idle_add(self._update_movie_list)
        

