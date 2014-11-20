# -*- coding: utf-8 -*- 
from behave import *
import time

@given(u'Estoy en la página principal')
def step_impl(context):
    context.driver.get("http://localhost:8080/ipmdb.html")

@when(u'Le doy al botón desconectar')
def step_impl(context):
    context.disconnect = context.driver.find_element_by_id("logout-button")
    context.driver.implicitly_wait(20)
    context.disconnect.click()

@then(u'Me lleva a la página de login')
def step_impl(context):
    time.sleep(1) # Espera 1 segundo mínimo para que cargue la página
    print context.driver.current_url
    assert "http://localhost:8080/login.html" in context.driver.current_url
    context.driver.implicitly_wait(20) # espera 20 segundos
