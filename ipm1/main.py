#!/usr/bin/python3
from view import *

# model = Model()
# controller = Controller(model)
view = View()

view.start()
view.get_movie_list().append(["Matrix"])
view.get_movie_list().append(["La jungla de cristal"])
view.get_movie_list().append(["King Kong"])
