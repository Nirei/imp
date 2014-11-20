# -*- coding: utf-8 -*- 
from behave import *
import time

@given(u'Estoy en la página de login')
def step_impl(context):
    context.driver.get("http://localhost:8080/login.html")

@then(u'Me lleva a la página principal')
def step_impl(context):
    time.sleep(1) # Espera 1 segundo mínimo para que cargue la página
    print context.driver.current_url
    assert "http://localhost:8080/ipmdb.html" in context.driver.current_url
    context.driver.implicitly_wait(20) # espera 20 segundos

@then(u'Me lleva a la página de login')
def step_impl(context):
    time.sleep(1) # Espera 1 segundo mínimo para que cargue la página
    print context.driver.current_url
    assert "http://localhost:8080/login.html" in context.driver.current_url
    context.driver.implicitly_wait(20) # espera 20 segundos

    
@when(u'Introduzco credenciales correctas')
def step_impl(context):
    # si fallan se generan excepciones
    context.user = context.driver.find_element_by_id("username")
    context.password = context.driver.find_element_by_id("password")
    context.send = context.driver.find_element_by_id("loginButton")
    context.user.send_keys("andreu.barro");
    context.password.send_keys("p5JFBJrt");
    context.driver.implicitly_wait(20)
    context.send.click()

@when(u'Introduzco credenciales {user} y {password} incorrectas')
def step_impl(context, user, password):
    # si fallan se generan excepciones
    context.user = context.driver.find_element_by_id("username")
    context.password = context.driver.find_element_by_id("password")
    context.send = context.driver.find_element_by_id("loginButton")
    context.user.send_keys(user);
    context.password.send_keys(password);
    context.driver.implicitly_wait(20)
    context.send.click()

@then(u'Sigo en la página de login')
def step_impl(context):
    time.sleep(1) # Espera 1 segundo mínimo para que cargue la página
    print context.driver.current_url
    assert "http://localhost:8080/login.html" in context.driver.current_url
    context.driver.implicitly_wait(20) # espera 20 segundos

