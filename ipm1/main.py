#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import gettext
from model import *
from controller import *
from gi.repository import GObject

_ = gettext.gettext

# Localhost server
#model = Model('http://localhost:5000')
# General server
model = Model('http://ipm-movie-database.herokuapp.com')

controller = Controller(model)

controller.start()

