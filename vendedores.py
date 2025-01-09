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
    def checkEmail(mail):
        try:
           if eventos.Eventos.validarMail(mail):
                var.ui.txtemailven.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtemailven.setText(mail.lower())
           else:
                var.ui.txtemailven.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtemailven.setText(None)
                var.ui.txtemailven.setPlaceholderText("correo no válido")
                var.ui.txtemailven.setFocus()
        except Exception as error:
            print("error checkvendedor", error)

    def checkMovil(movil):
        try:
            if eventos.Eventos.validarMovil(movil):
                    var.ui.txtmovilven.setStyleSheet('background-color: rgb(255, 255, 239);')
            else:
                    var.ui.txtmovilven.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                    var.ui.txtmovilven.setText(None)
                    var.ui.txtmovilven.setPlaceholderText("móvil no válido")
                    var.ui.txtmovilven.setFocus()
        except Exception as error:
           print("error check vendedor", error)

    def altaVendedor(self):
        try:
            op = 0
            nuevoven = [var.ui.txtdniven.text(), var.ui.txtaltaven.text(), var.ui.txtnomven.text().title(),
                        var.ui.txtmovilven.text(),var.ui.txtemailven.text()]

            if nuevoven[0] != "" and nuevoven[2] != "" and nuevoven[2] != "" and nuevoven[5] != "":
                op = 1
                #if conexionserver.ConexionServer.altaCliente(nuevocli):
                if conexion.Conexion.altaVendedor(nuevoven) and op == 1:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText("Alta Vendedor en Base de Datos")
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Vendedores.cargaTablaVendedores(self)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Aviso")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    mbox.setText('Error Faltan Datos o Vendedor Existe')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Cancelar')
                    mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Error Faltan Datos')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Cancelar')
                mbox.exec()
        except Exception as e:
            print("error alta cliente", e)
            
    @staticmethod
    def cargaTablaVendedores(self):
        try:
            listadoven = conexion.Conexion.listadoVendedores(self)
            var.longven = len(listadoven)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            start_index = var.paginaven * var.vendedoresxpagina
            end_index = start_index + var.vendedoresxpagina
            listado_pagina = listadoven[start_index:end_index]
            index = 0
            for registro in listado_pagina:
                var.ui.tablaVendedores.setRowCount(index + 1)
                var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  "+ registro[5] + "  ")))
                var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaVendedores.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
                var.ui.tablaVendedores.item(index, 0).setTextAlignment( QtCore.Qt.AlignmentFlag.AlignCenter |
                                                                        QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaVendedores.item(index,1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index,2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                var.ui.tablaVendedores.item(index,3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 4).setTextAlignment( QtCore.Qt.AlignmentFlag.AlignCenter |
                                                                        QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1
        except Exception as e:
            print("error cargaVendedores", e)

    def cargaOneVendedor(self):
        try:
            fila = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneVendedor(datos[0])
            #registro = conexionserver.ConexionServer.datosOneCliente(str(datos[0]))
            registro = [x if x != 'None' else '' for x in registro]
            listado = [var.ui.lblDniven, var.ui.txtDnivev, var.ui.txtNomvev, var.ui.txtAltacli_2,
                       var.ui.lblBajacli_3, var.ui.txtMovilven, var.ui.txtEmailven]
            for i in range(len(listado)):
                if i == 6:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(str(registro[i]))
        except Exception as error:
            print("error cargaOneCliente", error)

    def bajaVendedor(self):
        try:
            op = True
            var.ui.lblBajaVendedor.setText(datetime.now().strftime("%d/%m/%Y"))
            datos = [var.ui.lblBajacli_3.text(),var.ui.txtDniVendedor.text()]
            if datos[1] != "":
                op = True
            else:
                op = False
            if op == True:
                conexion.Conexion.bajaVendedor(datos)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Vendedor Dado Baja")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Vendedores.cargaTablaVendedores(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Error: Vendedor no existe, Dado de Baja o Falta fecha Baja")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Vendedores.cargaTablaVendedores(self)
        except Exception as e:
            print("error baja Cliente", e)
