#LIBRERIAS NECESARIAS
try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract

import sys
import os
import webbrowser
import clipboard
import random
import shutil
import playsound
import re

from gtts import gTTS


from shutil import copyfile,copytree,copy2

#from googletrans import Translator Traductor de mala calidad

from translate import Translator

from PySide2.QtWebEngineWidgets import QWebEngineView

from PySide2.QtWidgets import *

from PySide2.QtCore import *

from PySide2.QtGui import *

from PySide2.QtSql import *

from PySide2.QtWebChannel import *

from PySide2.QtWebEngine import *

text_Input=None#Texto ingresado
lang_dec=""#Idioma detectado
html_file=[#Html para procesar
    "<!DOCTYPE html>","<html>","<style>","body {","display: flex;","flex-direction: column;",
    "justify-content: center;","min-height: 100vh;","}","</style>","<body>","<table>",    
    "</table>","</body>","</html>"
    ]
html_fileR=[#Html por defecto
    "<!DOCTYPE html>","<html>","<style>","body {","display: flex;","flex-direction: column;",
    "justify-content: center;","min-height: 100vh;","}","</style>","<body>","<table>",    
    "</table>","</body>","</html>"
    ]
html_part=[#Array con las traducciones  
]
text_web=None#Cuadro de texto para cargar codigo y visor HTML
tool3=None#Boton para cambiar entre texto y HTML
indexFhtml=12#Index iniciar tablas
_path_=""

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

class Form(QDialog):
    #Crear la interfaz del programa
    def __init__(self, parent=None):
        global text_Input
        global text_web
        global tool3
        global _path_
        super(Form, self).__init__(parent)
        # Create widgets y el layout central con los dos combobox y el boton       
        
        layout_arriba=QVBoxLayout() #Layout para todo lo de arriba
        layout_arribaIZ=QVBoxLayout()   #Layout para la izquierda con el texto Markdown y herramientas de edicion
        text_web=QTextEdit()
        text_web.setLineWrapColumnOrWidth(200)
        text_web.setLineWrapMode(QTextEdit.FixedColumnWidth)

        layout_AI_tools=QHBoxLayout()#Cuadro de herramientas para edicion de traduccion temporal  
        self.tool1=QPushButton("Título")   
        self.tool2=QPushButton("Párrafo")      
        tool3=QPushButton("Texto")
        self.tool4=QPushButton("Agregar") 
        layout_AI_tools.addWidget(self.tool1)   
        layout_AI_tools.addWidget(self.tool2)    
        layout_AI_tools.addWidget(tool3)  
        layout_AI_tools.addWidget(self.tool4)     
        layout_arribaIZ.addWidget(text_web)
        layout_arribaIZ.addLayout(layout_AI_tools)
        layout_arriba.addLayout(layout_arribaIZ,1)

        layout_arribaDE=QVBoxLayout()#Herramientas para la visualizacion de HTML  
        layout_AD_tools=QHBoxLayout()
        self.tool11=QPushButton("Nuevo")   
        self.tool22=QPushButton("Guardar")  
        self.tool33=QPushButton("Abrir")
        self.view_HTML = QWebEngineView()
        layout_AD_tools.addWidget(self.tool11)
        layout_AD_tools.addWidget(self.tool22)
        layout_AD_tools.addWidget(self.tool33)
        
        layout_arribaDE.addWidget(self.view_HTML)
        layout_arribaDE.addLayout(layout_AD_tools)
        _path_=os.getcwd()+"/index.html"
        layout_arriba.addLayout(layout_arribaDE,2)
        self.view_HTML.load(QUrl.fromLocalFile(_path_))
        self.view_HTML.show()

        layout_Intermedio=QHBoxLayout()#Herramientas de traduccion
        self.ini_lang=QComboBox()
        self.ini_lang.addItem("autodetect")
        self.ini_lang.addItem("ru")
        self.ini_lang.addItem("en")
        self.ini_lang.addItem("uk")
        self.ini_lang.addItem("es")
        self.final_lang=QComboBox()
        self.final_lang.addItem("es")
        self.final_lang.addItem("en")
        self.final_lang.addItem("ru")
        self.final_lang.addItem("uk")
        self.final_lang.setEditable(True)
        self.bnt_traducir = QPushButton("Traducir!") 
        self.bnt_cap = QPushButton("Capturar!") 
        self.bnt_capT = QPushButton("Capturar text!") 
        self.bntSpeakInput=QPushButton("Speak Input!")
        self.bntSpeakOutput=QPushButton("Speak Output!")
        layout_Intermedio.addWidget(self.ini_lang)
        layout_Intermedio.addWidget(self.bntSpeakInput)
        layout_Intermedio.addWidget(self.final_lang)
        layout_Intermedio.addWidget(self.bntSpeakOutput)
        layout_Intermedio.addWidget(self.bnt_capT)
        layout_Intermedio.addWidget(self.bnt_cap)
        layout_Intermedio.addWidget(self.bnt_traducir)

        layout_abajo=QHBoxLayout()#Layout con el texto de entrada y salida
        text_Input=QTextEdit("")
        bntSpeakInput=QPushButton("Speak Input!")
        bntSpeakOutput=QPushButton("Speak Output!")
        self.text_Output=QTextEdit("")
        
        layout_abajo.addWidget(text_Input)
        layout_abajo.addWidget(self.text_Output)

        layout_Contenedor=QVBoxLayout() #Añadir todos los contenedores layouts 
        layout_Contenedor.addLayout(layout_arriba)
        layout_Contenedor.addLayout(layout_Intermedio)
        layout_Contenedor.addLayout(layout_abajo)

        # Set dialog layout
        self.setLayout(layout_Contenedor)

        # Add button signal to greetings slot
        self.bnt_traducir.clicked.connect(self.traducir)
        self.bnt_cap.clicked.connect(self.capturar)
        self.bnt_capT.clicked.connect(self.capturarT)
        tool3.clicked.connect(self.cambiar_vista)
        self.tool2.clicked.connect(self.setParrafo)
        self.tool1.clicked.connect(self.setTitulo)
        self.tool4.clicked.connect(self.insert2HTML)
        self.tool11.clicked.connect(self.newFileHTML)
        self.tool22.clicked.connect(self.saveHTMLFile)
        self.tool33.clicked.connect(self.AbrirHTML)

        self.bntSpeakInput.clicked.connect(self.SpeakInput)
        self.bntSpeakOutput.clicked.connect(self.SpeakOutput)

    def SpeakInput(self):
        if self.ini_lang.currentText()!="autodetect":
            tts = gTTS(text=text_Input.toPlainText(), lang=self.ini_lang.currentText())
            tts.save("audio.mp3")
            playsound.playsound('audio.mp3', True)
            os.remove("audio.mp3")
        else:
            QMessageBox.information(self, 'JTraductor', "Seleccione el idioma!")
    def SpeakOutput(self):
        ttss = gTTS(text=self.text_Output.toPlainText(), lang=self.final_lang.currentText())
        ttss.save("audio.mp3")
        playsound.playsound('audio.mp3', True)
        os.remove("audio.mp3")

    #Abrir en documentos.
    def AbrirHTML(self):
        global indexFhtml
        global _path_  
        global html_file     
        
        files=QFileDialog.getOpenFileName(self,"JTraductor","")
        if files[0]!="":
            self.newFileHTML()
            f=open(os.path.realpath(files[0]),"r")
            html_file=f.readlines()
            indexFhtml=len(html_file)-3
            _path_=files[0]
            self.view_HTML.load(QUrl.fromLocalFile(_path_))
            self.view_HTML.show()
            os.chdir(os.path.dirname(_path_))

        #for x in os.listdir(os.path.dirname(os.path.realpath(files[0]))+"/img"):
        #webbrowser.open("index.html")

    #Save HTML File
    def saveHTMLFile(self):        
        path=QFileDialog.getSaveFileName(self,"JTraductor","")
        f=open(path[0],"w")
        #f.writelines(html_file)
        for x in html_file:
            f.write(x+"\r\n")
        f.close()
        os.mkdir(os.path.dirname(os.path.realpath(path[0]))+"/img")
        copytree("./img",os.path.dirname(os.path.realpath(path[0]))+"/img",False,None)

    #New HTML file
    def newFileHTML(self):
        global html_file
        global indexFhtml
        global html_part
        _path_=os.getcwd()+"/index.html"
        f=open(_path_,"w")
        f.close()
        self.view_HTML.reload()
        indexFhtml=12
        html_part.clear()
        html_file=html_fileR.copy()
        for x in os.listdir(os.path.dirname(_path_)+'/img'):
            os.remove(os.path.dirname(_path_)+"/img/"+str(x))

    #Insertar to HTML
    def insert2HTML(self):
        global html_part
        global html_file
        global indexFhtml
        global _path_
        #print("c. index: "+str(indexFhtml)+" tamaño del vector: "+str(len(html_file))+" parte a insertar: "+str(html_part))
        html_file[indexFhtml:indexFhtml]=html_part        
        f=open(_path_,"w",encoding="utf-8")

        for x in html_file:
            f.write(x+"\r\n")
        f.close()


        indexFhtml+=8
        #print("c. index: "+str(indexFhtml)+" tamaño del vector: "+str(len(html_file))+" parte a insertar: "+str(html_part))
        self.view_HTML.reload()

    #Set titulo
    def setTitulo(self):
        global html_part
        html_part[2]=html_part[2].replace("<p>","<h2>")
        html_part[2]=html_part[2].replace("</p>","</h2>")

    #Set parrafo
    def setParrafo(self):
        global html_part
        html_part[2]=html_part[2].replace("<h2>","<p>")
        html_part[2]=html_part[2].replace("</h2>","</p>")

    #Cambiar vista HTML y texto
    def cambiar_vista(self):
        global text_web
        global tool3
        if tool3.text() =="HTML":
            text_tag=""
            for tag in html_part:
                text_tag+=tag+"\n"
            text_web.setPlainText(text_tag)
            tool3.setText("Texto")
        else:
            text_tag=""
            for tag in html_part:
                text_tag+=tag+"\n"
            text_web.setText(text_tag)
            tool3.setText("HTML")

    #Capturar texto por screenshot y traducir
    def capturar(self): 
        global lang_dec
        global text_Input
        lang_dec=self.ini_lang.currentText()
        #Visualizar
        self.showCaptura2record = ShowCaptura2record(self)
        self.showCaptura2record.showFullScreen()
        self.showCaptura2record.show()
        print(os.getcwd())
        
    def capturarT(self):
        #Get the clipboard
        global text_Input
        text_input="os"
        if os.name =='nt':
            text_input=clipboard.paste().replace("\r\n"," ")
        elif os.name=='posix':
            text_input=clipboard.paste().replace("\n"," ")
        text_input=text_input.strip()
        if not text_input[-1:] == '.':
            text_input+="."        
        text_Input.setText(text_input)

    # Capturar, optimizar y traducir
    def traducir(self):   
        global text_Input  
        global html_part  
        global text_web

        text_input="os"
        if os.name =='nt':
            text_input=text_Input.toPlainText().replace("\r\n"," ")
        elif os.name=='posix':
            text_input=text_Input.toPlainText().replace("\n"," ")
        text_input=text_input.strip()
        if not text_input[-1:] == '.':
            text_input+="."        
        text_Input.setText(text_input)

        traducir=Translator(from_lang=str(self.ini_lang.currentText()),to_lang=str(self.final_lang.currentText()))
        #print(text_Input.toPlainText())
        traduccion=""
        text_traducir=str(text_Input.toPlainText()).split('.')
        for k in text_traducir:
            print(k+":\t"+traducir.translate(k)+"\n")
            traduccion+=traducir.translate(k)+". "
        #traduccion=traducir.translate(cad)
        traduccion=traduccion.replace(". .",".")
        print(traduccion)
        self.text_Output.setText(traduccion)
        html_part=[
        "<tr>",
            "<th>",
                "<p> "+ traduccion +" </p>",
            "</th>",
            "<th>",
                "<h6> "+ text_input +" </h6>",
            "</th>",
        "</tr>",
        ]
        text_tag=""
        for tag in html_part:
            text_tag+=tag+"\n"
        text_web.setPlainText(text_tag)

class ShowCaptura2record(QDialog):#Clase para capturar pantalla y analizar texto o extraer imagen.
    def __init__(self, parent=None):
        super(ShowCaptura2record,self).__init__(parent)  
        pixmap=QScreen.grabWindow(app.primaryScreen(), app.desktop().winId())
        self.captura=QLabel(self)  
        self.captura.setPixmap(pixmap)
        
    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        global text_Input
        global lang_dec       
         
        global html_part  
        global text_web
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        cropQPixmap = self.captura.pixmap().copy(currentQRect)
        cropQPixmap.save('output.png')

        lang_detec=lang_dec
        if lang_detec=="ru":
            lang_detec+="s"
        elif lang_detec=="uk":
            lang_detec+="r"
        else:
            lang_detec="spa"

        if os.name =='nt':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'        

        text_Input.setText(pytesseract.image_to_string(Image.open('output.png'),lang=lang_detec))

        ShowCaptura2record.close(self)

        capturaSIN = QMessageBox.question(self, 'JTraductor', "¿Desea ingresar como imagen?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) 
        
        if capturaSIN == QMessageBox.Yes:
            imagen_test=str(random.random()*100)
            copyfile("output.png",os.path.dirname(_path_)+"/img/"+imagen_test)
            html_part=[
                    "<tr>",
                    "<th>", 
                    "<p> <img src=\"./img/"+ imagen_test +"\"/> </p>",
                    "</th>",
                    "<th>",
                    "<h6> <img src=\"./img/"+ imagen_test +"\"/> </h6>",
                    "</th>",
                    "</tr>",
                    ]
            text_tag=""
            for tag in html_part:
                text_tag+=tag+"\n"
            text_web.setPlainText(text_tag)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.setWindowFlags(Qt.WindowStaysOnTopHint)
    form.setWindowTitle("JTraductor")
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())