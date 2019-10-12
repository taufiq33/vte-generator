## GUI

import xlsxwriter
import time
import datetime
import sqlite3

dbObject = sqlite3.connect('config-db.db')
dbCursor = dbObject.cursor()

def getKadaluarsaConfig():
    query = "SELECT kadaluarsa FROM config WHERE id=1"
    return dbCursor.execute(query).fetchone()[0]

def getPathConfig():
    query = "SELECT generated_file_path FROM config WHERE id=1"
    return dbCursor.execute(query).fetchone()[0]

def updateConfig(kadaluarsa, folder):
    query = "UPDATE config SET kadaluarsa=? , generated_file_path=? WHERE id=1"
    dbCursor.execute(query, (kadaluarsa, folder))
    dbObject.commit()
    return True


class ExcelFile():
    """Kelas utama file excel yang akan di generate"""

    def __init__(self, kodeproduk, deskripsi, jumlah):
        self.kodeproduk = kodeproduk.upper()
        self.deskripsi = deskripsi.upper()
        self.jumlah = jumlah
        self.tanggalwaktu = time.strftime('%m/%d/%Y %H:%M', time.localtime(time.time()))
        self.tanggalwaktuFile = time.strftime('%d-%B-%Y %H%M', time.localtime(time.time()))
        self.kadaluarsa = getKadaluarsaConfig()
        self.folder = getPathConfig()
        self.ObjExcelFile = xlsxwriter.Workbook(self.folder + self.getNamaFile())
        self.worksheet = self.ObjExcelFile.add_worksheet()

    def getNamaFile(self) :
        namafile = "%s %s %s pcs.xlsx" % (self.kodeproduk, self.tanggalwaktuFile, self.jumlah)
        return namafile

    def generateExcelFile(self) :
        data = self.createArrayData()
        return self.createExcelFile(data)

    def createArrayData(self) :
        x = 1
        tanggalwaktuInFile = time.strftime('%m/%d/%Y %H:', time.localtime(time.time()))
        dataExcelVoucher = [];
        detikan = 0
        menitan = 0
        detikanInFile = 0
        menitanInFile = 0
        while x <= int(self.jumlah) :
            if detikan == 60 :
                detikanInFile = 0
                detikan = 0
                menitanInFile = int(menitanInFile) + 1
            else :
                menitanInFile = int(menitanInFile)
                detikanInFile = detikan
            if int(detikanInFile) < 10 :
                detikanInFile = '0' + str(detikanInFile)
            if int(menitanInFile) < 10 :
                menitanInFile = '0' + str(menitanInFile)
            dataExcelVoucher.append(
                [self.kodeproduk, '', self.deskripsi, '1',
                str(tanggalwaktuInFile) + str(menitanInFile) + ':' + str(detikanInFile),
                self.kadaluarsa]
            )
            # pesan = "generate baris %s " % (x)
            # time.sleep(0.005)
            # print(pesan)
            x = x + 1
            detikan = int(detikan) + 1
        dataExcelVoucher = tuple(dataExcelVoucher)
        return dataExcelVoucher


    def createExcelFile(self, arrayData) :
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        formattext = self.ObjExcelFile.add_format()
        formattext.set_num_format('@') # == text in excel

        # Iterate over the data and write it out row by row.
        for kp,kv,desk,kode,tgl,kada in (arrayData):
            self.worksheet.write(row, col,kp)
            self.worksheet.write(row, col + 1,kv,formattext)
            self.worksheet.write(row, col + 2,desk)
            self.worksheet.write(row, col + 3,kode)
            self.worksheet.write(row, col + 4,tgl)
            self.worksheet.write(row, col + 5,kada)
            row += 1

        self.worksheet.set_column('B:B', 25) ## set lebar kolom
        self.worksheet.set_column('E:E', 25)
        self.worksheet.set_column('F:F', 25)

        format1 = self.ObjExcelFile.add_format({'bg_color':  '#E60000','font_color': '#000000'})

        self.worksheet.conditional_format('B1:B200', {'type':'duplicate','format': format1}) ## otomatis deteksi duplikasi data

        self.ObjExcelFile.close()
        return True;
