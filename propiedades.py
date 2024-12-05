import var
import conexion
from PyQt6 import QtWidgets, QtGui, QtCore


class Propiedades():
    def altaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
            elif not registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Propiedad Existente')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Cancelar')
                mbox.exec()
            var.dlggestion.ui.txtGestipoprop.setText("")
        except Exception as e:
            print(f"Error: {e}")

    def bajaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            if conexion.Conexion.bajaTipoprop(tipo):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Tipo Propiedad Eliminada')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Propiedad No Existe')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Salir')
                mbox.exec()
            registro = conexion.Conexion.cargarTipoprop(self)
            var.ui.cmbTipoprop.clear()
            var.ui.cmbTipoprop.addItems(registro)
        except Exception as e:
            print(f"Error: {e}")

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtAltaprop.text(), var.ui.txtDirprop.text(),
                         var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(), var.ui.spnHabprop.text(),
                         var.ui.spnBanprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioalquilerprop.text(), var.ui.txtPrecioventaprop.text(),
                         var.ui.txtCPprop.text(),var.ui.txtObservaprop.toPlainText()
                         ]
            tipooper = []
            if var.ui.chkAlquiprop.isChecked():
                tipooper.append(var.ui.chkAlquiprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipooper.append(var.ui.chkInterprop.text())
            tipooper = "-".join(tipooper)
            propiedad.append(tipooper)
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquiprop.isChecked():
                propiedad.append(var.ui.rbtAlquiprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                propiedad.append(var.ui.rbtVentaprop.text())
            propiedad.append(var.ui.txtNomeprop.text())
            propiedad.append(var.ui.txtMovilprop.text())
            if conexion.Conexion.altaPropiedad(propiedad):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Propiedad Guardada')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            Propiedades.cargaTablaPropiedades(self)
        except Exception as e:
            print("error alta propiedad", e)

    @staticmethod
    def cargaTablaPropiedades(self):
        try:
            listado = conexion.Conexion.listadoPropiedades(self)
            var.longprop = len(listado)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            start_index = var.paginaprop * var.propiedadesxpagina
            end_index = start_index + var.propiedadesxpagina
            listado_pagina = listado[start_index:end_index]
            index = 0
            for registro in listado_pagina:
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[6]))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                if registro[10] == "":
                    registro[10] = "-"
                elif registro[11] == "":
                    registro[11] = "-"
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[10]+ " €"))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[11]+ " €"))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(registro[14]))
                var.ui.tablaPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaPropiedades.item(index,0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaPropiedades.item(index,2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaPropiedades.item(index,3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaPropiedades.item(index,8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1
        except Exception as e:
            print("error cargaTablaCientes", e)

    def cargaOnepropiedad(self):
        try:
            var.ui.chkAlquiprop.setChecked(False)
            var.ui.chkVentaprop.setChecked(False)
            var.ui.chkInterprop.setChecked(False)
            fila = var.ui.tablaPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.cargaOnepropiedad(str(datos[0]))
            # registro = conexionserver.ConexionServer.datosOneCliente(str(datos[0]))
            propiedad = [var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                         var.ui.cmbProvprop, var.ui.cmbMuniprop, var.ui.cmbTipoprop, var.ui.spnHabprop,
                         var.ui.spnBanprop, var.ui.txtSuperprop, var.ui.txtPrecioalquilerprop,
                         var.ui.txtPrecioventaprop, var.ui.txtCPprop, var.ui.txtObservaprop ]
            var.ui.lblCodprop.setText(str(registro[0]))
            for i  in range(len(propiedad)):
                if i == 3 or i == 4 or i == 5:
                    propiedad[i].setCurrentText(str(registro[i +1]))
                elif i == 6 or i == 7:
                    propiedad[i].setValue(int(registro[i +1]))
                elif i == 8:
                    propiedad[i].setText(str(registro[i +1]) + " m2")
                elif i == 9 or i == 10:
                    propiedad[i].setText(str(registro[i + 1]) + " €")
                else:
                    propiedad[i].setText(str(registro[i + 1]))
            if "Alquiler" in registro[14]:
                var.ui.chkAlquiprop.setChecked(True)
            if "Venta" in registro[14]:
                var.ui.chkVentaprop.setChecked(True)
            if "Intercambio" in registro[14]:
                var.ui.chkInterprop.setChecked(True)
            if registro[15] == "Disponible":
                var.ui.rbtDisponprop.setChecked(True)
            elif registro[15] == "Alquilado":
                var.ui.rbtAlquiprop.setChecked(True)
            elif registro[15] == "Vendido":
                var.ui.rbtVentaprop.setChecked(True)
            var.ui.txtNomeprop.setText(str(registro[16]))
            var.ui.txtMovilprop.setText(str(registro[17]))

        except Exception as error:
            print("error cargaOneCliente", error)

    def bajaPropiedad(self):
        try:
            novoestado = ""
            if var.ui.rbtAlquiprop.isChecked():
                novoestado = var.ui.rbtAlquiprop.text()
            if var.ui.rbtVentaprop.isChecked():
                novoestado = var.ui.rbtVentaprop.text()

            if var.ui.txtBajaprop.text() == "" or var.ui.rbtDisponprop.isChecked():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Falta Fecha Baja o Marcar Vendido o Alquilado')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText('Cancelar')
                mbox.exec()
            elif conexion.Conexion.bajaPropiedad(var.ui.txtBajaprop.text(), var.ui.lblCodprop.text(), novoestado):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setText('Propiedad Eliminada')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print(error)

    def historicoProp(self):
        try:
            if var.ui.chkHistoricoprop.isChecked():
                var.historiaprop = 0
            else:
                var.historiaprop = 1
            Propiedades.cargaTablaPropiedades(self)
        except Exception as Error:
            print("checkbox histórico", Error)

    def modificarPropiedad(self):
        try:
            op = True
            modifprop = [var.ui.lblCodprop.text(), var.ui.txtAltaprop.text(), var.ui.txtBajaprop.text(),
                         var.ui.txtDirprop.text().title(), var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(), var.ui.spnHabprop.text(), var.ui.spnBanprop.text(),
                         var.ui.txtSuperprop.text().split(' ')[0], var.ui.txtPrecioalquilerprop.text().split(' ')[0],
                         var.ui.txtPrecioventaprop.text().split(' ')[0], var.ui.txtCPprop.text(),var.ui.txtObservaprop.toPlainText() ]
            tipooper = []
            if var.ui.chkAlquiprop.isChecked():
                tipooper.append(var.ui.chkAlquiprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipooper.append(var.ui.chkInterprop.text())
            tipooper = "-".join(tipooper)
            modifprop.append(tipooper)
            if var.ui.rbtDisponprop.isChecked():
                modifprop.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquiprop.isChecked():
                modifprop.append(var.ui.rbtAlquiprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                modifprop.append(var.ui.rbtVentaprop.text())
            modifprop.append(var.ui.txtNomeprop.text().title())
            modifprop.append(var.ui.txtMovilprop.text())
            # if conexionserver.ConexionServer.modifCliente(modifcli) and op == True:
            if conexion.Conexion.modifPropiedad(modifprop):
                if var.ui.txtBajaprop.text() == "":
                    var.ui.rbtDisponprop.setChecked(True)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Datos Propiedad Modificados")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Faltan datos obligatorios o Propiedad no Existe.")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            Propiedades.cargaTablaPropiedades(self)

        except Exception as error:
            print("error modifPropiedad", error)

    def buscaProp(self):
        try:
            busqueda = [var.ui.cmbTipoprop.currentText(), var.ui.cmbMuniprop.currentText()]
            listado = conexion.Conexion.buscaProp(busqueda)
            if not listado:
                index = 0
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem("No hay registros para mostrar"))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem(""))
                var.ui.tablaPropiedades.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            else:
                index = 0
                for registro in listado:
                    var.ui.tablaPropiedades.setRowCount(index + 1)
                    var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[5]))
                    var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[6]))
                    var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                    var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                    if registro[10] == "":
                        registro[10] = "-"
                    elif registro[11] == "":
                        registro[11] = "-"
                    var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[10] + " €"))
                    var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[11] + " €"))
                    var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(registro[15]))
                    var.ui.tablaPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2])))
                    var.ui.tablaPropiedades.item(index, 0).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 1).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 2).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 3).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 4).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 5).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 6).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 7).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    var.ui.tablaPropiedades.item(index, 8).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                    index += 1
        except Exception as error:
            print("error buscaProp", error)

    def checkVenta(self):
        try:
            var.ui.chkVentaprop.setChecked(True)
            if var.ui.txtPrecioventaprop.text() == "":
                var.ui.chkVentaprop.setChecked(False)
        except Exception as error:
            print(error)

    def checkAlquiler(self):
        try:
            var.ui.chkAlquiprop.setChecked(True)
            if var.ui.txtPrecioalquilerprop.text() == "":
                var.ui.chkAlquiprop.setChecked(False)
        except Exception as error:
            print(error)