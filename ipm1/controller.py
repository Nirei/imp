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
        dialog = self._builder.get_object("error-dialog")
        # Ugly hack to edit dialog message
        dialog.get_children()[0].get_children()[0].get_children()[1].get_children()[1].set_text(message)
        dialog.run()
        
        dialog.destroy()


    def __init__(self, model):
        super(Controller, self).__init__()
        self._model = model
        self._builder = Gtk.Builder()
        self._builder.add_from_file("interfaz1.glade")
        self._builder.connect_signals(self)
        
        self._show_login_dialog(True)
    
    def run(self):
        Gtk.main()
    
    ###### HANDLERS!! ######
    
    # Login dialog handlers
    def on_login_dialog_close(self, *args):
        Gtk.main_quit(*args)
    
    def on_dialog_login_button_clicked(self, widget):
        user = self._builder.get_object("user-entry").get_text()
        passwd = self._builder.get_object("passwd-entry").get_text()
        print("user: " + user)
        print("pass: " + passwd)
        self._model.login(self, user, passwd)

    # Windows handlers
    def on_exit(self, *args):
        Gtk.main_quit(*args)
    
    # Menu handlers
    
    # Toolbar handlers
    def on_add_movie(self, widget):
        print("on_button_add_clicked")
    
    def on_modify_movie(self, widget):
        print("on_button_modify_clicked")
    
    def on_delete_movie(self, widget):
        print("on_button_delete_clicked")
    
    def on_logout(self, widget):
        print("on_button_disconnect_clicked")
    
    # Content handlers
    def on_selection_changed(self, tso):
        (a,b) = tso.get_selected()
        print(a[b][0])
    
    ###### CALLBACKS!! ######
    
    def login_answer(self, *answer):
        if answer[0]:
            GObject.idle_add(self._show_login_dialog, false)
            GObject.idle_add(self._show_main_window, true)
        else:
            GObject.idle_add(self._show_error, answer[1])
    
    def request_done():
        pass
