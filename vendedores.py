from sys import exception
import conexion
from datetime import datetime
import conexionserver
import eventos
import var
from PyQt6 import QtWidgets, QtGui, QtCore

class Vendedores:
    def __init__(self):
        self.valor = 0

    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtdniven.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                var.ui.txtdniven.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtdniven.setText(None)
                var.ui.txtdniven.setFocus()
        except Exception as e:
            print("error check cliente", e)
