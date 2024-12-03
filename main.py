from xml.etree.ElementPath import prepare_parent

from venPrincipal import *
from venAux import *
import sys
import var
import conexion
import conexionserver
import eventos
import clientes
import styles
import propiedades

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = dlgGestionprop()
        var.dlgabout = dlgAbout()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        var.historico = 1
        var.historiaprop = 1
        var.paginacli = 0
        var.clientesxpagina = 15
        var.long = 0
        #conexionserver.ConexionServer.crear_conexion(self)
        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargaTablaPropiedades(self)

        '''
        eventos de tablas
        '''
        eventos.Eventos.resizeTablaClientes(self)
        eventos.Eventos.resizeTablaPropiedades(self)

        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        var.ui.tablaPropiedades.clicked.connect(propiedades.Propiedades.cargaOnepropiedad)


        '''
        
        zona de eventos del menubar y toolbar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionTipoPropiedades.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionactionBuscaprop.triggered.connect(propiedades.Propiedades.buscaProp)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVprop)
        var.ui.actionExportar_Propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONprop)
        var.ui.actionAcerca_de.triggered.connect(eventos.Eventos.abrirAbout)


        '''
        
        eventos de botones
        '''
        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnAltaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnModifcli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnDelprop.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnModifprop.clicked.connect(propiedades.Propiedades.modificarPropiedad)
        var.ui.btnBuscacli.clicked.connect(clientes.Clientes.buscaCli)
        var.ui.btnNextClie.clicked.connect(clientes.Clientes.nextCli)
        var.ui.btnPrevCli.clicked.connect(clientes.Clientes.prevCli)

        '''
              
        eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda: clientes.Clientes.checkMovil(var.ui.txtMovilcli.text()))
        var.ui.txtPrecioventaprop.textChanged.connect(propiedades.Propiedades.checkVenta)
        var.ui.txtPrecioalquilerprop.textChanged.connect(propiedades.Propiedades.checkAlquiler)
        '''
        
        eventos combobox
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargaMuniCli)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargaMuniprop)
        eventos.Eventos.cargarTipoprop(self)

        '''
        
        eventos checkbox
        '''
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoricoprop.stateChanged.connect(propiedades.Propiedades.historicoProp)
        var.ui.chkVentaprop.setEnabled(False)
        var.ui.chkAlquiprop.setEnabled(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
