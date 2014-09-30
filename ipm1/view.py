import threading
from gi.repository import Gtk

class Handler:
    # Windows handlers
    def on_delete_main_window(self, *args):
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


class View(threading.Thread):
    def __init__(self):
        super().__init__()
        self._builder = Gtk.Builder()
        self._builder.add_from_file("interfaz1.glade")
        self._builder.connect_signals(Handler())
        
        window = self._builder.get_object("main-window")
        window.show_all()
        
    def run(self):
        Gtk.main()
    
    def get_movie_list(self):
        return self._builder.get_object("movie-list")

