import threading
from gi.repository import Gtk

class View(threading.Thread):
    def __init__(self):
        super().__init__()
        self._builder = Gtk.Builder()
        self._builder.add_from_file("interfaz1.glade")
        self._builder.connect_signals(self)
        
        # window = self._builder.get_object("main-window")
        # window.show_all()
        
        login = self._builder.get_object("login-dialog")
        login.show_all()
        
    def run(self):
        Gtk.main()
    
    def get_movie_list(self):
        return self._builder.get_object("movie-list")
        
    # def show_error_dialog(self, *args):
    
    ###### HANDLERS!! ######
    
    # Login dialog handlers
    def on_login_dialog_close(self, *args):
        Gtk.main_quit(*args)
    
    def on_dialog_login_button_clicked(self, widget):
        print("user: " + self._builder.get_object("user-entry").get_text())
        print("pass: " + self._builder.get_object("passwd-entry").get_text())

    # Windows handlers
    def on_main_window_remove(self, *args):
        Gtk.main_quit(*args)
    
    # Menu handlers
    
    # Toolbar handlers
    def on_button_add_clicked(self, widget):
        print("on_button_add_clicked")
    
    def on_button_modify_clicked(self, widget):
        print("on_button_modify_clicked")
    
    def on_button_delete_clicked(self, widget):
        print("on_button_delete_clicked")
    
    def on_button_disconnect_clicked(self, widget):
        print("on_button_disconnect_clicked")
    
    # Content handlers
    def on_selection_changed(self, tso):
        (a,b) = tso.get_selected()
        print(a[b][0])
        

