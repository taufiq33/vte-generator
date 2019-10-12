from app import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settingWindow import *



class mainWindowApp(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self) :
        self.resize(750,150)
        self.move(300,300)
        self.setWindowTitle('VTE Generator - Voucher to Excel Generator')

        self.windowWidget = QWidget()
        self.setCentralWidget(self.windowWidget)
        self.windowWidget.formLayout = QGridLayout()
        self.windowWidget.btnLayout = QHBoxLayout()

        self.windowWidget.mainAppLayout = QVBoxLayout()
        self.windowWidget.appLabel = QLabel('VTE Generator - Voucher to Excel Generator')
        self.windowWidget.btnCreateFile = QPushButton('Buat File >>')
        self.windowWidget.btnPengaturan = QPushButton('Pengaturan >>')
        self.windowWidget.kodeProdukLabel = QLabel('Kode Produk')
        self.windowWidget.kodeProdukInput = QLineEdit()
        self.windowWidget.deskripsiLabel = QLabel('Deskripsi')
        self.windowWidget.deskripsiInput = QLineEdit()
        self.windowWidget.jumlahVoucherLabel = QLabel('Jumlah Voucher')
        self.windowWidget.jumlahVoucherInput = QLineEdit()

        self.windowWidget.mainAppLayout.addWidget(self.windowWidget.appLabel)
        self.windowWidget.formLayout.addWidget(self.windowWidget.kodeProdukLabel, 0, 0)
        self.windowWidget.formLayout.addWidget(self.windowWidget.kodeProdukInput, 0, 1)
        self.windowWidget.formLayout.addWidget(self.windowWidget.deskripsiLabel,1, 0)
        self.windowWidget.formLayout.addWidget(self.windowWidget.deskripsiInput,1, 1)
        self.windowWidget.formLayout.addWidget(self.windowWidget.jumlahVoucherLabel,2, 0)
        self.windowWidget.formLayout.addWidget(self.windowWidget.jumlahVoucherInput,2, 1)
        self.windowWidget.btnLayout.addWidget(self.windowWidget.btnPengaturan)
        self.windowWidget.btnLayout.addWidget(self.windowWidget.btnCreateFile)

        self.windowWidget.mainAppLayout.addLayout(self.windowWidget.formLayout)
        self.windowWidget.mainAppLayout.addLayout(self.windowWidget.btnLayout)
        self.windowWidget.mainAppLayout.addStretch()
        self.windowWidget.setLayout(self.windowWidget.mainAppLayout)


        self.statusBar().showMessage("Folder File : %s\n Setting Kadaluarsa : %s" % (getPathConfig(), getKadaluarsaConfig()))
        self.windowWidget.btnCreateFile.clicked.connect(self.createFileAction)
        self.windowWidget.btnPengaturan.clicked.connect(self.settingAction)

    def createFileAction(self) :
        kodeproduk = self.windowWidget.kodeProdukInput.text()
        deskripsi = self.windowWidget.deskripsiInput.text()
        jumlah = self.windowWidget.jumlahVoucherInput.text()

        if kodeproduk == ''  or deskripsi == '' or jumlah == '' :
            QMessageBox.critical(self, 'Error gannn!!!',
            'Isi data2 dengan lengkap ya gan!! jangan dikosongin'
            )
        else :
            file_baru = ExcelFile(kodeproduk, deskripsi, jumlah)

            print(file_baru.getNamaFile())

            if file_baru.generateExcelFile() :
                QMessageBox.information(self, 'Generate File Berhasil',
                'File "%s" sukses digenerate gannnn!!!'  % file_baru.getNamaFile()
                )
            self.windowWidget.kodeProdukInput.clear()
            self.windowWidget.deskripsiInput.clear()
            self.windowWidget.jumlahVoucherInput.clear()

    def settingAction(self) :
        settingWindowApp = settingWindow()
        settingWindowApp.exec_()
