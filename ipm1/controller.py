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
    
    def _update_movie_list(self, number, page):
        self._movie_list.clear()
        self._label_page.set_text(str(number))
        for movie in page:
            # TODO: Maneras más eficientes de rellenar la lista??
            self._movie_list.append([movie['title']])
    
    def _update_nav_buttons_status(self, is_first, is_last):
        self._prev_button.set_sensitive(not is_first)
        self._next_button.set_sensitive(not is_last)
    
    def _display_movie(self, movie):
        if movie:
            self._movie_img.set_text(movie['url_image'])
            self._movie_title.set_text(movie['title'])
            self._movie_year.set_text(str(movie['year']))
            self._movie_desc.set_text(unicode(movie['synopsis']))
            self._movie_last_edit.set_text(movie['username'])
            self._movie_category.set_text(movie['category'])
        else:
            self._movie_img.set_text('')
            self._movie_title.set_text('')
            self._movie_year.set_text('')
            self._movie_desc.set_text('')
            self._movie_last_edit.set_text('')
            self._movie_category.set_text('')
            
    def _set_movie_data_editable(self, boolean):
        self._movie_list_view.set_sensitive(not boolean)
        
        # Menú
        self._menu_add.set_sensitive(not boolean)
        self._menu_modify.set_sensitive(not boolean)
        self._menu_delete.set_sensitive(not boolean)
        
        # Barra de herramientas
        self._add_button.set_sensitive(not boolean)
        self._modify_button.set_sensitive(not boolean)
        self._delete_button.set_sensitive(not boolean)
        
        # Zona de edición
        self._movie_img.set_editable(boolean)
        self._movie_img.set_can_focus(boolean)
        self._movie_title.set_editable(boolean)
        self._movie_title.set_can_focus(boolean)
        self._movie_year.set_editable(boolean)
        self._movie_year.set_can_focus(boolean)
        self._movie_category.set_editable(boolean)
        self._movie_category.set_can_focus(boolean)
        self._movie_desc_view.set_editable(boolean)
        self._movie_desc_view.set_can_focus(boolean)
        self._movie_desc_view.set_cursor_visible(boolean)
       
        self._edit_tools.set_visible(boolean)
        self._image_paste.set_sensitive(boolean)
    
    def _read_movie(self):
        start, end = self._movie_desc.get_bounds()
        try:
            year = int(self._movie_year.get_text())
        except:
            # El año no es un número
            self._show_error('El año introducido no es válido')
            return None
        
        return {
            'url_image' : self._movie_img.get_text(),
            'title'     : self._movie_title.get_text(),
            'year'      : year,
            'category'  : self._movie_category.get_text(),
            'synopsis'      : self._movie_desc.get_text(start, end, False) 
        }
    
    def _read_row(self):
        sel = self._movie_list_view.get_selection()
        paths = sel.get_selected_rows()[1]
        if paths:
            return paths[0].get_indices()[0]
        else:
            return None
    
    ### CONSTRUCTOR & INHERITED METHODS ###

    def __init__(self, model):
        super(Controller, self).__init__()
        self._model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file('gui.glade')
        self._builder.connect_signals(self)
        
        # Important interface elements
        self._menu_add = self._builder.get_object('file-add')
        self._menu_modify = self._builder.get_object('file-modify')
        self._menu_delete = self._builder.get_object('file-delete')
               
        self._add_button = self._builder.get_object('button-add')
        self._modify_button = self._builder.get_object('button-modify')
        self._delete_button = self._builder.get_object('button-delete')
        
        self._movie_list = self._builder.get_object('movie-list')
        self._movie_list_view = self._builder.get_object('movie-list-view')
        self._label_page = self._builder.get_object('label-page')
        self._next_button = self._builder.get_object('button-next')
        self._prev_button = self._builder.get_object('button-prev')
        self._edit_tools = self._builder.get_object('editcontrols')
        self._image_copy = self._builder.get_object('url-copy')
        self._image_paste = self._builder.get_object('url-paste')

        self._movie_img = self._builder.get_object('movie-img')
        self._movie_title = self._builder.get_object('movie-title')
        self._movie_desc = self._builder.get_object('movie-synopsis')
        self._movie_desc_view = self._builder.get_object('movie-desc')
        self._movie_year = self._builder.get_object('movie-year')
        self._movie_last_edit = self._builder.get_object('movie-last-edit')
        self._movie_category = self._builder.get_object('movie-category')
        
        self._restore_cursor = 0
        self._adding = False
        
        self._show_login_dialog(True)
    
    def run(self):
        GObject.threads_init()
        Gtk.main()
    
    ###### HANDLERS!! ######
    
    # Login dialog handlers
    def on_login_dialog_close(self, *args):
        Gtk.main_quit(*args)
    
    def on_login(self, widget):
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
        if self._model.is_logged_in():
            self._model.logout(self)
        Gtk.main_quit(*args)
    
    # Toolbar handlers
    def on_add_movie(self, widget):
        self._adding = True
        
        # Save cursor
        if paths:
            self._restore_cursor = self._read_row()
        # And unset cursor
        sel.unselect_all()
        
        # Clear all fields
        self._display_movie(None)
        # Make data editable
        self._set_movie_data_editable(True)
        # And set the username
        self._movie_last_edit.set_text(self._model.get_username())
        
    def on_modify_movie(self, widget):
        self._adding = False
        
        # Make data editable
        self._set_movie_data_editable(True)
    
    def on_delete_movie(self, widget):
        self._model.delete_movie(self, self._read_row())
    
    def on_edit_cancel(self, widget):
        # Lock editable fields
        self._set_movie_data_editable(False)
        # And restore cursor (this triggers the loading of the movie data)
        self._movie_list_view.set_cursor(self._restore_cursor)
        
        # If modifyin, reload movie data
        if not self._adding:
            self._model.get_movie(self._read_row())
    
    def on_edit_accept(self, widget):
        # If we are adding a new movie
        if self._adding:
            self._model.add_movie(self, self._read_movie())
        # If modifying an existing one
        else:
            # Send new info to model
            self._model.modify_movie(self, self._read_row(), self._read_movie())
    
    def on_logout(self, widget):
        self._model.logout(self)
    
    # Content handlers
    def on_selection_changed(self, sel):
        row = self._read_row()
        # If a movie is selected, display it's info
        if row is not None:
            self._model.get_movie(self, row)
        # else ignore the event
    
    def nav_prev(self, widget):
        self._model.prev_page()
        self._model.get_list(self)
    
    def nav_next(self, widget):
        self._model.next_page()
        self._model.get_list(self)
    
    ###### CALLBACKS!! ######
    # Estas funciones son para llamar desde el modelo, de modo que si realizan
    # cambios en la interfaz deben hacerlo a traves de GObject.idle_add()
    
    def login_answer(self, *args):
        # Success
        if args[0]:
            GObject.idle_add(self._show_login_dialog, False)
            GObject.idle_add(self._show_main_window, True)
            self._model.get_list(self)
            # Load first movie
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

    def page_request_answer(self, success, *args):
        if success:
            GObject.idle_add(self._update_movie_list, args[0], args[1])
            GObject.idle_add(self._update_nav_buttons_status, args[2], args[3])
            # Load first movie
            GObject.idle_add(self._movie_list_view.set_cursor, 0)
            
        else:
            GObject.idle_add(self._show_error, args[0])
    
    def movie_request_answer(self, success, answer):
        if success:
            GObject.idle_add(self._display_movie, answer)
        else:
            GObject.idle_add(self._show_error, answer)
    
    def add_request_answer(self, success, *args):
        # Success
        if success:
            GObject.idle_add(self._set_movie_data_editable, False)
            # Update movie list
            self._model.get_list(self)
        # Failure
        else:
            GObject.idle_add(self._show_error, args[0])
    
    def modify_request_answer(self, success, *args):
        # Success
        if success:
            GObject.idle_add(self._set_movie_data_editable, False)
            # Update movie list
            self._model.get_list(self)
        # Failure
        else:
            GObject.idle_add(self._show_error, args[0])
    
    def delete_request_answer(self, success, *args):
        # Success
        if success:
            # Update movie list
            self._model.get_list(self)
        # Failure
        else:
            GObject.idle_add(self._show_error, args[0])
            
        

