##CLI

import xlsxwriter
import time
import datetime

kodeproduk = input('masukkan kode produk : ')
deskripsi = input('masukkan deskripsi : ')
jumlah = input('masukkan jumlah voucher : ')
tanggalwaktu = time.strftime('%m/%d/%Y %H:%M', time.localtime(time.time()))
tanggalwaktuFile = time.strftime('%d-%B-%Y %H:%M', time.localtime(time.time()))

kodeproduk = kodeproduk.upper()
deskripsi = deskripsi.upper()

namafile = "%s %s %s pcs.xlsx" % (kodeproduk, tanggalwaktuFile, jumlah)
folder = "generated_file/"

workbook = xlsxwriter.Workbook(folder + namafile)
worksheet = workbook.add_worksheet()

x = 1
tanggalwaktuInFile = time.strftime('%m/%d/%Y %H:', time.localtime(time.time()))
dataExcelVoucher = [];
detikan = 0
menitan = 0
detikanInFile = 0
menitanInFile = 0
while x <= int(jumlah) :
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
        [kodeproduk, '', deskripsi, '1',
        str(tanggalwaktuInFile) + str(menitanInFile) + ':' + str(detikanInFile),
        '12/27/2020 10:44:03']
    )
    pesan = "generate baris %s " % (x)
    time.sleep(0.005)
    print(pesan)
    x = x + 1
    detikan = int(detikan) + 1
dataExcelVoucher = tuple(dataExcelVoucher)


# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

formattext = workbook.add_format()
formattext.set_num_format('@') # == text in excel

# Iterate over the data and write it out row by row.
for kp,kv,desk,kode,tgl,kada in (dataExcelVoucher):
    worksheet.write(row, col,kp)
    worksheet.write(row, col + 1,kv,formattext)
    worksheet.write(row, col + 2,desk)
    worksheet.write(row, col + 3,kode)
    worksheet.write(row, col + 4,tgl)
    worksheet.write(row, col + 5,kada)
    row += 1

worksheet.set_column('B:B', 25) ## set lebar kolom
worksheet.set_column('E:E', 25)
worksheet.set_column('F:F', 25)

format1 = workbook.add_format({'bg_color':  '#E60000','font_color': '#000000'})

worksheet.conditional_format('B1:B200', {'type':'duplicate','format': format1}) ## otomatis deteksi duplikasi data

workbook.close()
print("---[[[[]]]]---"*200)
print("File sukses dibuat !!!")
print("Nama file : %s " % namafile)
