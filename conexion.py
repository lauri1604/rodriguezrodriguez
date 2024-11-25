import os

from PyQt6 import QtSql, QtWidgets, QtCore
import sqlite3

import var
from datetime import datetime
class Conexion:

    '''

    GESTIÓN CLIENTES
    metodo STATICMETHOD que no depende de la instancia de una clase
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase. 
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    '''

    @staticmethod
    def db_conexion(self = None):
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                               QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    @staticmethod
    def listaProv(self =None):
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias "
                          " where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def altaCliente(nuevocli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into CLIENTES (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, "
                          " dircli, provcli, municli ) VALUES (:dnicli, :altacli, :apelcli, :nomecli, "
                          " :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli",str(nuevocli[1]))
            query.bindValue(":apelcli",str(nuevocli[2]))
            query.bindValue(":nomecli",str(nuevocli[3]))
            query.bindValue(":emailcli",str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error alta cliente", e)
        except sqlite3.IntegrityError:
            return False

    def listadoClientes(self):
        try:
            listado = []
            if var.historico == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM CLIENTES WHERE bajacli is NULL ORDER BY apelcli, nomecli ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            elif var.historico == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM CLIENTES ORDER BY apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado

        except Exception as e:
            print("error listado en conexion", e)


    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM CLIENTES WHERE dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro

        except Exception as e:
            print("error datos un cliente", e)

    def modifCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    if query.exec():
                        query = QtSql.QSqlQuery()
                        query.prepare("UPDATE clientes set altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, "
                                      " emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli = :provcli, "
                                      " municli = :municli, bajacli = :bajacli where dnicli = :dni")
                        query.bindValue(":dni", str(registro[0]))
                        query.bindValue(":altacli", str(registro[1]))
                        query.bindValue(":apelcli", str(registro[2]))
                        query.bindValue(":nomecli", str(registro[3]))
                        query.bindValue(":emailcli", str(registro[4]))
                        query.bindValue(":movilcli", str(registro[5]))
                        query.bindValue(":dircli", str(registro[6]))
                        query.bindValue(":provcli", str(registro[7]))
                        query.bindValue(":municli", str(registro[8]))
                        if registro[9] == "":
                            query.bindValue(":bajacli", QtCore.QVariant())
                        else:
                            query.bindValue(":bajacli", str(registro[9]))
                        if query.exec():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        except Exception as error:
            print("error modificar cliente", error)

    def bajaCliente(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(datos[1]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    query = QtSql.QSqlQuery()
                    query.prepare("UPDATE clientes set bajacli = :bajacli where dnicli = :dnicli")
                    query.bindValue(":bajacli", str(datetime.now().strftime("%d/%d/%Y")))
                    query.bindValue(":dnicli", str(datos[1]))
                    if query.exec():
                        return True
                    else:
                        return False
        except Exception as e:
            print("error baja cliente en conexion", e)

    def buscaCli(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select * from clientes where dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error baja cliente en conexion", e)


    '''
    
        GESTIÓN PROPIEDADES
        metodo STATICMETHOD que no depende de la instancia de una clase
        Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase. 
        Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    '''


    def listaProv(self=None):
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov


    @staticmethod
    def listaMuniProv(provincia):
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias "
                          " where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def altaTipoprop(tipo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into TIPOPROPIEDAD (TIPO) VALUES (:tipo) ")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                registro = Conexion.cargarTipoprop(self = None)
                return registro
            else:
                return registro
        except Exception as error:
            print("error alta tipo propiedad", error)

    def bajaTipoprop(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) from TIPOPROPIEDAD WHERE tipo = :tipo")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                if query.next() and query.value(0)>0:
                    query = QtSql.QSqlQuery()
                    query.prepare("DELETE from TIPOPROPIEDAD where tipo = :tipo")
                    query.bindValue(":tipo", str(tipo))
                    if query.exec():
                        return True
                else:
                    return False
        except Exception as error:
            print("error baja tipo propiedad", error)

    def cargarTipoprop(self):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * from TIPOPROPIEDAD ORDER BY tipo ASC")
            if query.exec():
                while query.next():
                    registro.append(str(query.value(0)))
            return registro
        except Exception as error:
            print("error cargar tipo propiedad", error)

    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(" INSERT into PROPIEDADES(altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, "
                          " superprop, prealquiprop, prevenprop, cpprop, obserprop, tipooper, estadoprop, nomeprop, movilprop) "
                          " VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop, :banprop, :superprop, "
                          " :prealquiprop, :prevenprop, :cpprop, :obserprop, :tipooper, :estadoprop, :nomeprop, :movilprop)"
            )
            query.bindValue(":altaprop", str(propiedad[0]))
            query.bindValue(":dirprop", str(propiedad[1]))
            query.bindValue(":provprop", str(propiedad[2]))
            query.bindValue(":muniprop", str(propiedad[3]))
            query.bindValue(":tipoprop", str(propiedad[4]))
            query.bindValue(":habprop", int(propiedad[5]))
            query.bindValue(":banprop", int(propiedad[6]))
            query.bindValue(":superprop", str(propiedad[7]))
            query.bindValue(":prealquiprop", str(propiedad[8]))
            query.bindValue(":prevenprop", str(propiedad[9]))
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":obserprop", str(propiedad[11]))
            query.bindValue(":tipooper", str(propiedad[12]))
            query.bindValue(":estadoprop", str(propiedad[13]))
            query.bindValue(":nomeprop", str(propiedad[14]))
            query.bindValue(":movilprop", str(propiedad[15]))
            if query.exec():
                return True
            elif not query.exec():
                return False
        except Exception as error:
            print("error alta propiedad en conexion", error)

    def listadoPropiedades(self):
        try:
            listado = []
            if var.historiaprop == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM PROPIEDADES WHERE bajaprop is NULL ORDER BY muniprop ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            elif var.historiaprop == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM PROPIEDADES ORDER BY muniprop ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as error:
            print("error listado propiedades en conexion", error)

    def bajaPropiedad(fecha, codigo, estado):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades set bajaprop = :fecha, estadoprop = :estado where codigo = :codigo")
            query.bindValue(":fecha", str(fecha))
            query.bindValue(":codigo", str(codigo))
            query.bindValue(":estado", str(estado))
            if query.exec():
                return True
        except Exception as error:
            print("error baja propiedad en conexion", error)

    def cargaOnepropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM PROPIEDADES where codigo = :codigo")
            query.bindValue(":codigo", int(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as error:
            print("error carga propiedad en conexion", error)

    def modifPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE PROPIEDADES SET altaprop = :altaprop, bajaprop = :bajaprop, dirprop = :dirprop, provprop = :provprop, "
                " muniprop = :muniprop, tipoprop = :tipoprop, habprop = :habprop, banprop = :banprop, superprop = :superprop, "
                " prealquiprop = :prealquiprop, prevenprop = :prevenprop, cpprop = :cpprop, obserprop = :obserprop, "
                " tipooper = :tipooper, estadoprop = :estadoprop, nomeprop = :nomeprop, movilprop = :movilprop "
                " WHERE codigo = :codigo")
            query.bindValue(":codigo", int(propiedad[0]))
            query.bindValue(":altaprop", str(propiedad[1]))
            if propiedad[2] == "":
                query.bindValue(":bajaprop",QtCore.QVariant())
            else:
                query.bindValue(":bajaprop", str(propiedad[2]))
            query.bindValue(":dirprop", str(propiedad[3]))
            query.bindValue(":provprop", str(propiedad[4]))
            query.bindValue(":muniprop", str(propiedad[5]))
            query.bindValue(":tipoprop", str(propiedad[6]))
            query.bindValue(":habprop", int(propiedad[7]))
            query.bindValue(":banprop", int(propiedad[8]))
            query.bindValue(":superprop", str(propiedad[9]))
            query.bindValue(":prealquiprop", str(propiedad[10]))
            query.bindValue(":prevenprop", str(propiedad[11]))
            query.bindValue(":cpprop", str(propiedad[12]))
            query.bindValue(":obserprop", str(propiedad[13]))
            query.bindValue(":tipooper", str(propiedad[14]))
            query.bindValue(":estadoprop", str(propiedad[15]))
            query.bindValue(":nomeprop", str(propiedad[16]))
            query.bindValue(":movilprop", str(propiedad[17]))
            if query.exec():
                return True
            elif not query.exec():
                return False
        except Exception as error:
            print("error alta propiedad en conexion", error)

    def buscaProp(datos):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM PROPIEDADES WHERE estadoprop= :estadoprop and tipoprop = :tipoprop and muniprop = :muniprop "
                          " ORDER BY codigo ")
            query.bindValue(":tipoprop", str(datos[0]))
            query.bindValue(":muniprop", str(datos[1]))
            query.bindValue(":estadoprop", "Disponible")
            if query.exec():
                while query.next():
                    prop = []
                    for i in range(query.record().count()):
                        prop.append(str(query.value(i)))
                    registro.append(prop)
            return registro
        except Exception as error:
            print("error busca propiedad en conexion", error)