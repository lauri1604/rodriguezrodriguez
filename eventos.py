import os
import re
import sys
import csv
import json
from venAux import *
from datetime import datetime
import locale
import clientes
import eventos
import propiedades
import var
import time
import conexion
import zipfile
import shutil
import conexionserver
from PyQt6 import QtWidgets, QtGui


#Establecer configuración regional

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')

class Eventos:
    @staticmethod
    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
        mbox.setWindowTitle('Salir')
        mbox.setText('¿Desea Salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        mbox.resize(600, 800) #no funciona si no usa QDialgo QmessageBox lo tienen bloqueado
        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProv(self):
        try:
            var.ui.cmbProvcli.clear()
            var.ui.cmbProvprop.clear()
            listado = conexion.Conexion.listaProv(self)
            #listado = conexionserver.ConexionServer.listaProv(self)
            var.ui.cmbProvcli.addItems(listado)
            var.ui.cmbProvprop.addItems(listado)
        except Exception as e:
            print("error carga provincias: ", e)

    def cargaMuniCli(self):
        try:
            provincia = var.ui.cmbProvcli.currentText()
            listado = conexion.Conexion.listaMuniProv(provincia)
            #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
            var.ui.cmbMunicli.clear()
            var.ui.cmbMunicli.addItems(listado)
        except Exception as e:
            print("error carga municipios: ", e)

    def cargaMuniprop(self):
        provincia = var.ui.cmbProvprop.currentText()
        listado = conexion.Conexion.listaMuniProv(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMuniprop.clear()
        var.ui.cmbMuniprop.addItems(listado)

    def validarDNI(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as error:
            print("error en validar dni ", error)

    def abrirCalendar(btn):
        try:
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if  var.ui.panPrincipal.currentIndex() == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.ui.panPrincipal.currentIndex() == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.ui.panPrincipal.currentIndex()  == 1 and var.btn == 0:
                var.ui.txtAltaprop.setText(str(data))
            elif var.ui.panPrincipal.currentIndex() == 1 and var.btn == 1:
                var.ui.txtBajaprop.setText(str(data))

            time.sleep(0.2)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail =="":
            return True
        else:
            return False
    def validarMovil(movil):
        regex =  r"^[67]\d{8}$"
        if re.match(regex, movil):
            return True
        else:
            return False

    def resizeTablaClientes(self):
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if (i == 1 or i == 2 or i == 4 or i == 5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tablaPropiedades.horizontalHeader()
            for i in range(header.count()):
                if (i == 1 or i == 2):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            #header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    def crearBackup(self):
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia = str(fecha)+'_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, '.zip')
            var.dlgabrir.centrarEnPantalla()
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, 'w')
                fichzip.write('bbdd.sqlite', os.path.basename('bbdd.sqlite'), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Copia Seguridad')
                mbox.setText("Copia Seguridad Creada")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("error en crear backup: ", error)

    def restaurarBackup(self):
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurar Copia Seguridad", '',
                                                    '*.zip;;All Files(*)')
            file = filename[0]   # Obtiene la ruta del archivo
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Copia Seguridad')
                mbox.setText("Copia Seguridad Restaurada")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                conexion.Conexion.db_conexion(self)
                eventos.Eventos.cargarProv(self)
                clientes.Clientes.cargaTablaCientes(self)
        except Exception as error:
            print("error en resturar backup: ", error)


    def limpiarPanel(self):
        try:
            objetospanelcli = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli, var.ui.txtEmailcli,
                        var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli, var.ui.cmbMunicli, var.ui.txtBajacli]
            for i,dato in enumerate(objetospanelcli):
                if i == 7 or i == 8:
                    pass
                else:
                    dato.setText("")
            eventos.Eventos.cargarProv(self)
            var.ui.cmbMunicli.clear()
            clientes.Clientes.cargaTablaClientes(self)
            objetospanelprop = [var.ui.lblCodprop, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                             var.ui.txtSuperprop, var.ui.txtPrecioalquilerprop, var.ui.txtPrecioventaprop,
                             var.ui.txtCPprop, var.ui.txtObservaprop, var.ui.txtNomeprop, var.ui.txtMovilprop ]
            for i,dato in enumerate(objetospanelprop):
                dato.setText("")
            var.ui.cmbProvprop.clear()
            eventos.Eventos.cargarProv(self)
            var.ui.cmbMuniprop.clear()
            eventos.Eventos.cargaMuniprop(self)
            var.ui.cmbTipoprop.clear()
            eventos.Eventos.cargarTipoprop(self)
            var.ui.spnHabprop.setValue(0)
            var.ui.spnBanprop.setValue(0)
            var.ui.chkAlquiprop.setEnabled(False)
            var.ui.chkVentaprop.setEnabled(False)
            var.ui.chkInterprop.setEnabled(False)
            propiedades.Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print("error en limpiar panel: ", error)

    def abrirTipoprop(self):
        try:
            var.dlggestion.show()
        except Exception as error:
            print("error en abrir gestion propiedades ", error)

    def cargarTipoprop(self):
        registro = conexion.Conexion.cargarTipoprop(self)
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(registro)

    def exportCSVprop(self):
        try:
            var.historiaprop = 0
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_DatosPropiedades.csv')
            directorio, fichero = var.dlgabrir.getSaveFileName(None,"Exporta Datos en CSV" , file, '.csv')
            if fichero:
                registros = conexion.Conexion.listadoPropiedades(self)
                print(registros)
                with open(fichero, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)  # creo el puntero de almacenamiento
                    writer.writerow(["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio", "Tipo",
                                     "NºHabitaciones", "NºBaños", "Superficie", "Precio Alquiler", "Precio Compra",
                                     "Código Postal", "Observaciones", "Operación", "Estado", "Propietario", "Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Error')
                mbox.setText("Error Exportación de Datos Propiedades")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("error en exportar cliente ", error)

    def exportJSONprop(self):
        try:
            var.historiaprop = 0
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_DatosPropiedades.json')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en JSON", file, '.json')
            if fichero:
                keys = ["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio", "Tipo",
                                 "NºHabitaciones", "NºBaños", "Superficie", "Precio Alquiler", "Precio Compra",
                                 "Código Postal", "Observaciones", "Operación", "Estado", "Propietario", "Móvil"]
                registros = conexion.Conexion.listadoPropiedades(self)
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonfile:
                    json.dump(lista_propiedades, jsonfile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Error')
                mbox.setText("Error Exportación de Datos Propiedades")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("error en exportar cliente ", error)

    def abrirAbout(self):
        var.dlgabout.show()

    def cerrarAbout(self):
        var.dlgabout.hide()