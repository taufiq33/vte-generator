from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import app
import os

class settingWindow(QDialog) :
    def __init__(self) :
        super().__init__()
        self.setupUi()

    def setupUi(self) :
        self.resize(650,150)
        self.move(300,300)
        self.setWindowTitle('Pengaturan')

        self.formLayout = QGridLayout()
        self.btnLayout = QHBoxLayout()

        self.mainAppLayout = QVBoxLayout()
        self.btnBatal = QPushButton('Batal')
        self.btnSimpan = QPushButton('Simpan Pengaturan')
        self.folderFileLabel = QLabel('Folder file ')
        self.folderFileInput = QLineEdit()
        self.kadaluarsaLabel = QLabel('Waktu kadaluarsa')
        self.kadaluarsaInput = QLineEdit()
        self.btnPilihFolder = QPushButton('Ubah Folder >>')
        self.helpKadaluarsa = QLabel("bulan/tanggal/tahun jam:menit:detik")
        self.helpFolder = QLabel("Folder tempat file akan disimpan")
        self.folderFileInput.setText(app.getPathConfig())
        self.kadaluarsaInput.setText(app.getKadaluarsaConfig())


        self.formLayout.addWidget(self.kadaluarsaLabel,0, 0)
        self.formLayout.addWidget(self.kadaluarsaInput,0, 1)
        self.formLayout.addWidget(self.helpKadaluarsa,0, 2)
        self.formLayout.addWidget(self.folderFileLabel, 1, 0)
        self.formLayout.addWidget(self.folderFileInput, 1, 1)
        self.formLayout.addWidget(self.helpFolder,1, 2)
        self.formLayout.addWidget(self.btnPilihFolder,2, 1)
        self.btnLayout.addWidget(self.btnBatal)
        self.btnLayout.addWidget(self.btnSimpan)

        self.mainAppLayout.addLayout(self.formLayout)
        self.mainAppLayout.addLayout(self.btnLayout)
        self.mainAppLayout.addStretch()
        self.setLayout(self.mainAppLayout)

        self.btnBatal.clicked.connect(lambda: self.close())
        self.btnPilihFolder.clicked.connect(self.pilihFolderAction)
        self.btnSimpan.clicked.connect(self.simpanSettingAction)

    def pilihFolderAction(self) :
        self.dirName = QFileDialog.getExistingDirectory(self, 'Pilih Folder', os.curdir, QFileDialog.ShowDirsOnly)
        if not self.dirName : return
        self.folderFileInput.setText(self.dirName + "/")

    def simpanSettingAction(self) :
        if self.folderFileInput.text() == ''  or self.kadaluarsaInput.text() == '':
            QMessageBox.critical(self, 'Error gannn!!!',
            'Isi data2 dengan lengkap ya gan!! jangan dikosongin'
            )
            self.close()
            return
        f = open('config.py', 'w')
        setting = """generated_file_path = '%s'\nkadaluarsa = '%s'
        """ % (self.folderFileInput.text(), self.kadaluarsaInput.text())
        if f.write(setting) :
            QMessageBox.information(self, 'Simpan Pengaturan Berhasil',
            'Pengaturan Berhasil disimpan juragan, silahkan tutup aplikasi dan buka kembali utk mengaplikasikan pengaturan barunya!!!'
            )
        f.close()
        self.close()
