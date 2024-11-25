from datetime import datetime
from dlgCalendar import *
import var
import eventos
from dlgGestionprop import *
import propiedades
from dlgAbout import *


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class dlgGestionprop(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionprop, self).__init__()
        self.ui = Ui_dlg_Tipoprop()
        self.ui.setupUi(self)
        self.ui.btnAltatipoprop.clicked.connect(propiedades.Propiedades.altaTipopropiedad)
        self.ui.btnDeltipoprop.clicked.connect(propiedades.Propiedades.bajaTipopropiedad)


class dlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(dlgAbout, self).__init__()
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        self.ui.btnCerrarAbout.clicked.connect(eventos.Eventos.cerrarAbout)
