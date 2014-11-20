Feature: Login en la aplicación web

  Login, comprobación de sesión y logout de la aplicación.
  La aplicación deberá ir a la página principal
  en cuanto reciba la cookie después del login, y viceversa
  al hacer logout.

  Scenario Outline: Login
     Given Estoy en la página de login
     When Introduzco credenciales <user> y <password>, que son <valor>
     Then Me lleva a la página principal si eran <valor>
     
     Examples:
       | user         | password     | valor      |
       | andreu.brao  | p5JFJBrt     | falsas     |
       | andreu.barro | falso        | falsas     |
       | andreu.barro | p5JFBJrt     | verdaderas |
       
  Scenario: Logout
     Given Estoy en la página principal
     When Le doy al botón desconectar
     Then Me lleva a la página de login
