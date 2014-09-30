#!/usr/bin/python3
from view import *

# model = Model()
# controller = Controller(model)
controller = Controller()

controller.start()
controller.get_movie_list().append(["Matrix"])
controller.get_movie_list().append(["La jungla de cristal"])
controller.get_movie_list().append(["King Kong"])
