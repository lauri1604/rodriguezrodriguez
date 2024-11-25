from sys import exception
import conexion
from datetime import datetime
import conexionserver
import eventos
import var
from PyQt6 import QtWidgets, QtGui, QtCore

class Clientes:
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("error check cliente", e)

    def checkEmail(mail):
        try:
           if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())
           else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()
        except Exception as error:
            print("error check cliente", error)

    def checkMovil(movil):
        try:
           if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilcli.setStyleSheet('background-color: rgb(255, 255, 239);')
           else:
                var.ui.txtMovilcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilcli.setText("Movil no válido")
                var.ui.txtMovilcli.setFocus()
        except Exception as error:
            print("error check cliente", error)

    def altaCliente(self):
        try:
            op = 0
            nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),
                 var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(),var.ui.cmbProvcli.currentText(),
                 var.ui.cmbMunicli.currentText()]

            if nuevocli[0] != "" and nuevocli[1] != "" and nuevocli[2] != "" and nuevocli[3] != ""  and nuevocli[5] != "" and nuevocli[6] != "" and nuevocli[7] != "" and nuevocli[8]!= "":
                op = 1

                #if conexionserver.ConexionServer.altaCliente(nuevocli):
                if conexion.Conexion.altaCliente(nuevocli) and op == 1:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText("Alta Cliente en Base de Datos")
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Aviso")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    mbox.setText('Error Faltan Datos o Cliente Existe')
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
    def cargaTablaClientes(self):
        try:
            listado = conexion.Conexion.listadoClientes(self)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str("  " + registro[5] + "  ")))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))
                var.ui.tablaClientes.item(index,0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                var.ui.tablaClientes.item(index,1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index,2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index,3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                var.ui.tablaClientes.item(index,4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index,5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index,6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1
        except Exception as e:
            print("error cargaTablaCientes", e)

    def cargaOneCliente(self):
        try:
            fila = var.ui.tablaClientes.selectedItems()

            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneCliente(str(datos[0]))
            #registro = conexionserver.ConexionServer.datosOneCliente(str(datos[0]))
            registro = [x if x != 'None' else '' for x in registro]
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                        var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli,var.ui.cmbProvcli,var.ui.cmbMunicli,
                       var.ui.txtBajacli]
            for i in range(len(listado)):
                if i == 7 or i == 8:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
        except Exception as error:
            print("error cargaOneCliente", error)

    def modifCliente(self):
        try:
            op = True
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                        var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(),
                        var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]
            for i, dato in enumerate(modifcli):
                if i == 4 or i == 9:
                    pass
                else:
                    if dato ==  "":
                        op = False
            #if conexionserver.ConexionServer.modifCliente(modifcli) and op == True:
            if  op == True:
                conexion.Conexion.modifCliente(modifcli)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Datos Cliente Modificados")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Faltan datos obligatorios o Cliente no Existe.")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
        except Exception as error:
            print("error modifCliente", error)

    def bajaCliente(self):
        try:
            op = True
            datos = [var.ui.txtBajacli.text(),var.ui.txtDnicli.text()]
            if datos[1] != "":
                op = True
            else:
                op = False
            if op == True:
                (conexion.Conexion.bajaCliente(datos))
                var.ui.txtBajacli.setText(datetime.now().strftime("%d/%d/%Y"))
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Cliente Dado Baja")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Error: Cliente no existe, Dado de Baja o Falta fecha Baja")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("error baja Cliente", e)

    def historicoCli(self):
        try:
            if var.ui.chkHistoriacli.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            Clientes.cargaTablaClientes(self)
        except exception as Error:
            print("checkbox histórico", Error)

    def buscaCli(self):
        try:
            registro = conexion.Conexion.buscaCli(str(var.ui.txtDnicli.text()))
            if registro:
                # registro = conexionserver.ConexionServer.datosOneCliente(str(datos[0]))
                listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                           var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli]

                for i in range(len(listado)):
                    listado[i].setText(str(registro[i]))

                var.ui.cmbProvcli.setCurrentText(str(registro[7]))
                var.ui.cmbMunicli.setCurrentText(str(registro[8]))
                var.ui.txtBajacli.setText(str(registro[9]))

            else:
                dato = str(var.ui.txtDnicli.text())
                mensaje = "Error: Cliente con DNI "  + str(dato) +  " no existe"
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText(mensaje)
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as e:
            print("error buscaCli", e)


