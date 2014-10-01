#!/usr/bin/python
from model import *
from controller import *

model = Model('localhost:5000')
controller = Controller(model)

controller.start()
controller.get_movie_list().append(["Matrix"])
controller.get_movie_list().append(["La jungla de cristal"])
controller.get_movie_list().append(["King Kong"])
