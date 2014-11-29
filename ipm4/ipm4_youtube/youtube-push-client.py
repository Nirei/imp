#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GObject, WebKit
import templates
import os

PATH=os.path.dirname(os.path.realpath(__file__))

class PushWindow(Gtk.Window):

    def __init__(self):        
        Gtk.Window.__init__(self, title="YT Player")
        self.set_default_size(800, 600)
        self.create_widgets()
        self.connect_signals()
        
    def create_widgets(self):
        vbox = Gtk.Box(spacing=2, orientation=Gtk.Orientation.VERTICAL)
                
        self.webview = WebKit.WebView()     
        
        settings = WebKit.WebSettings()
        settings.set_property('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')  # Hack for loading the youtube player in older webkit versions!
        self.webview.set_settings(settings)           
        
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.add(self.webview)
        vbox.pack_start(scrolledWindow, True, True, 1)
               
        self.statusbar = Gtk.Statusbar()
        vbox.pack_start(self.statusbar, False, False, 1)        
        
        self.add(vbox)

    def connect_signals(self):
        self.connect("delete_event", Gtk.main_quit)        
        

    def start(self):
        self.show_all()
        self.webview.load_html_string(templates.video_page, "file://" + PATH + "/")
        Gtk.main()
    

if __name__=="__main__":
    win = PushWindow()
    win.start()
    

