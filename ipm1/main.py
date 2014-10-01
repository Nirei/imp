#!/usr/bin/python
from model import *
from controller import *

model = Model('http://localhost:5000')
controller = Controller(model)

controller.start()
