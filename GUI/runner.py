from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.checkbox import CheckBox
from kivy.config import Config
from functools import partial
from time import sleep
from functools import partial
import app

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', '200')

allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
            'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
            '7', '8', '9', ',']

class StartWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.kodeVoucher = Label(text='Kode Voucher')
        self.kodeVoucherInput = TextInput(multiline=False, write_tab=False, 
                        hint_text="Gunakan koma untuk prefix file. Contoh: VTDR2,PERTAMA")
        self.deskripsi = Label(text='Deskripsi Voucher')
        self.deskripsiInput = TextInput(multiline=False, write_tab=False)
        self.jumlahVoucher = Label(text='Jumlah Voucher')
        self.jumlahVoucherInput = TextInput(multiline=False, write_tab=False)
        self.settingButton = Button(text="Pengaturan")
        self.createButton = Button(text="Generate File")
        self.folderLabel = Label(text=f"Folder = {app.getPathConfig()}")
        self.kadaluarsaLabel = Label(text=f"Kadaluarsa = {app.getKadaluarsaConfig()}")

        self.add_widget(self.kodeVoucher )
        self.add_widget(self.kodeVoucherInput )
        self.add_widget(self.deskripsi )
        self.add_widget(self.deskripsiInput )
        self.add_widget(self.jumlahVoucher )
        self.add_widget(self.jumlahVoucherInput)
        self.add_widget(self.settingButton)
        self.add_widget(self.createButton)
        self.add_widget(self.folderLabel)
        self.add_widget(self.kadaluarsaLabel)

        self.settingButton.bind(on_press=self.settingEvent)
        self.createButton.bind(on_press=self.createEvent)

    def settingEvent(self, instance):
        vte_app.screen_manager.current = 'Setting'

    def createEvent(self, instance):

        kv = self.kodeVoucherInput.text
        desk = self.deskripsiInput.text
        jumlah = self.jumlahVoucherInput.text

        if kv is '' or desk is '' or jumlah is '' :
            popLayout = GridLayout()
            popLayout.cols = 1
            popLayout.add_widget(Label(text="isi semuanya , jangan ada yang kosong"))
            btn = Button(text="Ok siap")
            popLayout.add_widget(btn)
            
            pop = Popup(
                title="Gagal",
                content=popLayout,
                auto_dismiss=False,
                size=(100,100)
            )
            pop.open()
            btn.bind(on_press=pop.dismiss)

        else :
            if self.checkKodeVoucher(kv) :
                fileVoucher = app.ExcelFile(kv, desk, jumlah)
                if fileVoucher.generateExcelFile() :
                    self.kodeVoucherInput.text = ""
                    self.deskripsiInput.text = ""
                    self.jumlahVoucherInput.text = ""
                    popLayout = GridLayout()
                    popLayout.cols = 1
                    popLayout.add_widget(Label(text=f"file {fileVoucher.getNamaFile()} berhasil dibuat"))
                    btn = Button(text="Ok siap")
                    popLayout.add_widget(btn)
                    
                    pop = Popup(
                        title="Berhasil",
                        content=popLayout,
                        auto_dismiss=False,
                        size=(100,100)
                    )
                    pop.open()
                    btn.bind(on_press=pop.dismiss)
            else :
                    popLayout = GridLayout()
                    popLayout.cols = 1
                    popLayout.add_widget(Label(text="hanya boleh ada huruf, angka, dan simbol koma di isian kode voucher"))
                    btn = Button(text="Ok siap")
                    popLayout.add_widget(btn)
                    
                    pop = Popup(
                        title="Cek kode voucher lagi",
                        content=popLayout,
                        auto_dismiss=False,
                        size=(100,100)
                    )
                    pop.open()
                    btn.bind(on_press=pop.dismiss)
    def checkKodeVoucher(self, kodevoucher):
        status = True
        for x in kodevoucher :
            if x not in allowed :
                status = False
                break
        return status
        
class SettingWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.folder = Label(text='Folder')
        self.folderInput = TextInput(multiline=False, write_tab=False, text=f"{app.getPathConfig()}")
        self.hintFolder = Label(text="contoh : \n D:/INPUT VOUCHER/NOVEMBER 2019/")
        self.kadaluarsa = Label(text='Kadaluarsa')
        self.kadaluarsaInput = TextInput(multiline=False, write_tab=False, text=f"{app.getKadaluarsaConfig()}")
        self.hintKadaluarsa = Label(text="Bulan/tanggal/tahun jam:menit:detik")
        self.batalButton = Button(text="Batal")
        self.simpanButton = Button(text="Simpan Pengaturan")

        self.add_widget(self.folder)
        self.add_widget(self.folderInput)
        self.add_widget(self.hintFolder)
        self.add_widget(self.kadaluarsa)
        self.add_widget(self.kadaluarsaInput)
        self.add_widget(self.hintKadaluarsa)
        self.add_widget(Label())
        self.add_widget(self.batalButton)
        self.add_widget(self.simpanButton)

        self.batalButton.bind(on_press=self.batalEvent)
        self.simpanButton.bind(on_press=self.simpanEvent)

    def batalEvent(self, instance):
        vte_app.screen_manager.current = "Start"
    
    def simpanEvent(self, instance):
        folder = self.folderInput.text
        kadaluarsa = self.kadaluarsaInput.text
        if app.updateConfig(kadaluarsa, folder) :
            print(f"Saved !{folder}, {kadaluarsa}")
            btn = Button(text="Ok gan")
            label = Label(text="Pengaturan berhasil disimpan, buka kembali aplikasi ya")
            popLayout = GridLayout()
            popLayout.cols = 1
            popLayout.add_widget(label)
            popLayout.add_widget(btn)

            pop = Popup(
                title="Berhasil",
                content=popLayout
            )
            btn.bind(on_press=App.get_running_app().stop)

            pop.open()

        vte_app.screen_manager.current = "Start"

    def pilihFolderEvent(self, instance):
        popLayout = GridLayout()
        popLayout.cols = 1
        popLayout.add_widget(FileChooserIconView())
        btnSimpan = Button(text="Pilih folder")
        btnBatal = Button(text="Batal")
        # popLayout.add_widget(btnSimpan)
        # popLayout.add_widget(btnBatal)

        pop = Popup(
            title="Pilih folder",
            content=popLayout,
            size_hint=(1,1),
            size=(500,500)
        )
        pop.open()

class VTEApp(App):
    def build(self):
        self.title = "VTE - Voucher to excel generator"
        self.screen_manager = ScreenManager()

        self.start_window = StartWindow()
        screen = Screen(name='Start')
        screen.add_widget(self.start_window)
        self.screen_manager.add_widget(screen)

        self.setting_window = SettingWindow()
        screen1 = Screen(name="Setting")
        screen1.add_widget(self.setting_window)
        self.screen_manager.add_widget(screen1)

        return self.screen_manager

if __name__ == "__main__":
    vte_app = VTEApp()
    vte_app.run()