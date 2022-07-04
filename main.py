#burada fotoğraf editörü Easy Editor oluşturun!
from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap 
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import*

app = QApplication([])
pencerem = QWidget()       
pencerem.resize(700, 500) 
pencerem.setWindowTitle("Foto Editor")
gorsel_yeri = QLabel("Görsel")
dosya_butonu = QPushButton("Dosya")
gorsel_listesi = QListWidget()

btn_sol = QPushButton("Sol")
btn_sag = QPushButton("Sağ")
btn_ayna = QPushButton("Ayna")
btn_keskin = QPushButton("Keskinlik")
btn_siyahbeyaz = QPushButton("S/B")
satir = QHBoxLayout()          # Ana satır
sutun1 = QVBoxLayout()         #iki sütuna bölünebilir
sutun2 = QVBoxLayout()
sutun1.addWidget(dosya_butonu)      # birinci dizin seçme tuşudur.
sutun1.addWidget(gorsel_listesi)     #ve dosyaların listesi
sutun2.addWidget(gorsel_yeri) #ikinci resimde

butonlar_satiri = QHBoxLayout()    # ve tuş dizisi
butonlar_satiri.addWidget(btn_sol)
butonlar_satiri.addWidget(btn_sag)
butonlar_satiri.addWidget(btn_ayna)
butonlar_satiri.addWidget(btn_keskin)
butonlar_satiri.addWidget(btn_siyahbeyaz)
sutun2.addLayout(butonlar_satiri)

satir.addLayout(sutun1,20)
satir.addLayout(sutun2,80)
pencerem.setLayout(satir)

pencerem.show()

klasor_yolu = ""
def filtrele(dosyalar,uzantilar):
     calisilacak_gorseller_listesi = []
     for dosya in dosyalar:
          for uzanti in uzantilar:
               if dosya.endswith(uzanti):
                    calisilacak_gorseller_listesi.append(dosya)
     return calisilacak_gorseller_listesi

def klasor_sec():
     global klasor_yolu
     klasor_yolu= QFileDialog.getExistingDirectory()

def gorselleri_goster():

     uzantilar = [".jpg",".png",".jpeg",".gif",".bmp",".PNG"]
     klasor_sec()
     dosya_adlari = filtrele(os.listdir(klasor_yolu),uzantilar)
     gorsel_listesi.clear()
     for dosya in dosya_adlari:
         gorsel_listesi.addItem(dosya)

dosya_butonu.clicked.connect(gorselleri_goster)


class GoruntuIsleyici():
     def __init__(self):
          self.gorsel= None
          self.klasor = None
          self.dosya_adi = None 
          self.degistirilen_gorsel_klasoru = "degistirilmis/"

     def gorsel_yukleme_fonk(self, g_klasor, g_dosya_adi):
          self.klasor = g_klasor
          self.dosya_adi = g_dosya_adi
          gorsel_adresi = os.path.join(g_klasor,g_dosya_adi)
          self.gorsel = Image.open(gorsel_adresi)
     
     def gosterme_fonk(self, adres):
          gorsel_yeri.hide()
          gosterilecek_gorsel=QPixmap(adres)
          genislik=gorsel_yeri.width()
          yukseklik=gorsel_yeri.height()
          gosterilecek_gorsel=gosterilecek_gorsel.scaled(genislik,yukseklik,Qt.KeepAspectRatio)
          gorsel_yeri.setPixmap(gosterilecek_gorsel)
          gorsel_yeri.show()


     def sb_yap(self): #istasyon siyah beyaz yapan istasyon/fonk
          self.gorsel = self.gorsel.convert("L")
          self.kaydet()
          gorsel_adresi = os.path.join(self.klasor, self.degistirilen_gorsel_klasoru,
              self.dosya_adi)
          self.gosterme_fonk(gorsel_adresi)

     def sola_cevir(self):
          self.gorsel= self.gorsel.transpose(Image.ROTATE_90)
          self.kaydet()
          gorsel_adresi= os.path.join(self.klasor, self.degistirilen_gorsel_klasoru,
              self.dosya_adi)
          self.gosterme_fonk(gorsel_adresi)

     def saga_cevir(self):
          self.gorsel= self.gorsel.transpose(Image.ROTATE_270)
          self.kaydet()
          gorsel_adresi= os.path.join(self.klasor, self.degistirilen_gorsel_klasoru,
              self.dosya_adi)
          self.gosterme_fonk(gorsel_adresi)

     def ayna(self):
          self.gorsel= self.gorsel.transpose(Image.FLIP_LEFT_RIGHT)
          self.kaydet()
          gorsel_adresi= os.path.join(self.klasor, self.degistirilen_gorsel_klasoru,
              self.dosya_adi)
          self.gosterme_fonk(gorsel_adresi)

     def netlestir(self):
          self.gorsel= self.gorsel.filter(SHARPEN)
          self.kaydet()
          gorsel_adresi= os.path.join(self.klasor, self.degistirilen_gorsel_klasoru,
              self.dosya_adi)
          self.gosterme_fonk(gorsel_adresi)

     def kaydet(self):
          adres = os.path.join(self.klasor, self.degistirilen_gorsel_klasoru)
          if not(os.path.exists(adres) or os.path.isdir(adres)):
            os.mkdir(adres)
          gorsel_adresi = os.path.join(adres, self.dosya_adi)
          self.gorsel.save(gorsel_adresi)
 
gorsel_nesnesi= GoruntuIsleyici()

def secilenGorseliGoster():
     if gorsel_listesi.currentRow() >= 0:
          tiklanan_gorsel=gorsel_listesi.currentItem().text()
          gorsel_nesnesi.gorsel_yukleme_fonk(klasor_yolu,tiklanan_gorsel)
          gorsel_adresi = os.path.join(klasor_yolu,tiklanan_gorsel)
          gorsel_nesnesi.gosterme_fonk(gorsel_adresi)

gorsel_listesi.currentRowChanged.connect(secilenGorseliGoster)
btn_siyahbeyaz.clicked.connect(gorsel_nesnesi.sb_yap)
btn_sol.clicked.connect(gorsel_nesnesi.sola_cevir)
btn_sag.clicked.connect(gorsel_nesnesi.saga_cevir)
btn_ayna.clicked.connect(gorsel_nesnesi.ayna)
btn_keskin.clicked.connect(gorsel_nesnesi.netlestir)

app.exec()
