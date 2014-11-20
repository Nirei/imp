Feature: Login en la aplicación web

  Login, comprobación de sesión y logout de la aplicación.
  La aplicación deberá ir a la página principal
  en cuanto reciba la cookie después del login, y viceversa
  al hacer logout.

  Scenario: Login correcto
     Given Estoy en la página de login
     When Introduzco credenciales correctas
     Then Me lleva a la página principal
     
  Scenario Outline: Login incorrecto
     Given Estoy en la página de login
     When Introduzco credenciales <user> y <password> incorrectas
     Then Sigo en la página de login
     
     Examples:
       | user         | password     |
       | andreu.brao  | p5JFJBrt     |
       | andreu.barro | falso        |
       
  Scenario: Logout
     Given Estoy en la página principal
     When Le doy al botón desconectar
     Then Me lleva a la página de login
