from PyQt5 import QtCore, QtWidgets
from validate_email import validate_email
import client_ui
import connect_ui

import sys
import socket
import os

def separador(string,tam):
    return [string[:tam],string[tam+1:]]

class ReceiveThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, client_socket):
        super(ReceiveThread, self).__init__()
        self.client_socket = client_socket
        self.msg_rcv = True

    def run(self):
        while True:
            if self.msg_rcv == True:
                self.receive_message()

    def receive_message(self):
        message = self.client_socket.recv(1024)
        message = message.decode()

        print(message)
        self.signal.emit(message)



class Client(object):
    def __init__(self):
        self.messages = []
        self.mainWindow = QtWidgets.QMainWindow()

        # add widgets to the application window
        self.connectWidget = QtWidgets.QWidget(self.mainWindow)
        self.chatWidget = QtWidgets.QWidget(self.mainWindow)

        self.chatWidget.setHidden(True)
        self.chat_ui = client_ui.Ui_Form()
        self.chat_ui.setupUi(self.chatWidget)
        self.chat_ui.sendButton.clicked.connect(self.send_message)
        self.chat_ui.clearMsgButton.clicked.connect(self.chat_ui.messageBrowser.clear)
        self.chat_ui.clearSrvButton.clicked.connect(self.chat_ui.serverMsgBrowser.clear)  
        self.chat_ui.refreshButton.clicked.connect(self.send_refresh)

        self.connect_ui = connect_ui.Ui_Form()
        self.connect_ui.setupUi(self.connectWidget)
        self.connect_ui.connectButton.clicked.connect(self.btn_connect_clicked)

        self.mainWindow.setGeometry(QtCore.QRect(1080, 20,350, 500))
        self.mainWindow.show()

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
    def btn_connect_clicked(self):
        host = self.connect_ui.hostTextEdit.toPlainText()
        port = self.connect_ui.portTextEdit.toPlainText()
        nickname = self.connect_ui.nameTextEdit.toPlainText()
        nickname = nickname+"\n"
        email = self.connect_ui.emailTextEdit.toPlainText()
        email = email+"\n"
        local = self.connect_ui.localTextEdit.toPlainText()
        local = local+"\n"

        if len(host) == 0:
            host = "192.168.15.10"
        
        if len(port) == 0:
            port = 5900
        else:
            try:
                port = int(port)
            except Exception as e:
                error = "Invalid port number \n'{}'".format(str(e))
                print("[INFO]", error)
                self.show_error("Port Number Error", error)
        
        if len(nickname) < 1:
            nickname = socket.gethostname()
        
        if len(local) < 1:
            local = "undefined"

        nickname = nickname
        local = local

        if validate_email(email.strip('\n')):
            if self.connect(host, port, nickname, email, local):
                self.connectWidget.setHidden(True)
                self.chatWidget.setVisible(True)

                self.recv_thread = ReceiveThread(self.tcp_client)
                self.recv_thread.signal.connect(self.show_message)
                self.recv_thread.start()
                print("[INFO] recv thread started")
        else:
            print("[INFO] ")
            self.show_error("Invalid Email", "Unable to connect to server")
            self.connect_ui.emailTextEdit.clear()


    def show_message(self, message):
        _translate = QtCore.QCoreApplication.translate
        if message[:3] == "#cl":
            self.chat_ui.serverMsgBrowser.append(message[3:])
        elif message[:3] == "#ul":
            self.chat_ui.userBrowser.clear()
            self.chat_ui.userBrowser.append(message[3:])
        elif message[:3] == "#gl":
            self.chat_ui.groupBrowser.clear()
            self.chat_ui.groupBrowser.append(message[3:])
        elif message[:3] == "#ch":
            self.chat_ui.messageBrowser.clear()
            self.chat_ui.canal.setText(_translate("Form", "Canal: "+message[3:]))
        else:
            self.chat_ui.messageBrowser.append(message)
        

    def connect(self, host, port, nickname, email, local):

        try:
            self.tcp_client.connect((host, port))
            self.tcp_client.send(nickname.encode())
            self.tcp_client.send(email.encode())
            self.tcp_client.send(local.encode())

            print("[INFO] Connected to server")

            return True
        except Exception as e:
            error = "Unable to connect to server \n'{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Connection Error", error)
            self.connect_ui.hostTextEdit.clear()
            self.connect_ui.portTextEdit.clear()
            
            return False
        

    def send_message(self):
        message = self.chat_ui.msgTextEdit.toPlainText()
        if message != "":
            self.chat_ui.messageBrowser.append("Me: " + message)

            print("sent: " + message)
            
            line = message.split()

            if line[0] == "/imagem":
                self.tcp_client.send("/imagem".encode())
                arqv = line[1][len("file:///"):]
                file = open(arqv,"rb")
                file_size = os.path.getsize(arqv)
                file_name = line[2]

                self.tcp_client.send(f"{file_name}.png {str(file_size)}".encode())

                data = file.read()
                self.tcp_client.sendall(data)
                self.tcp_client.send(b"<END>")
                self.chat_ui.msgTextEdit.clear()
                self.chat_ui.serverMsgBrowser.append("Digite qualquer mensagem para confirmar o envio da imagem")

                file.close()
                
            elif line[0] == "/audio":
                self.tcp_client.send("/audio".encode())
                arqv = line[1][len("file:///"):]
                file = open(arqv,"rb")
                file_size = os.path.getsize(arqv)
                file_name = line[2]

                self.tcp_client.send(f"{file_name}.mp3 {str(file_size)}".encode())

                data = file.read()
                self.tcp_client.sendall(data)
                self.tcp_client.send(b"<END>")
                self.chat_ui.msgTextEdit.clear()
                self.chat_ui.serverMsgBrowser.append("Digite qualquer mensagem para confirmar o envio da audio")

                file.close()

            elif line[0] == "/abrir":
                self.recv_thread.msg_rcv = False
                self.tcp_client.send(message.encode())
                file_size = self.recv_thread.client_socket.recv(1024)
                file_size = file_size.decode()
                print(file_size)
                file_size = int(file_size)

                file = open(line[1], "wb")
                file_bytes = self.recv_thread.client_socket.recv(file_size)
                file.write(file_bytes)
                file.close()
                self.recv_thread.msg_rcv  = True
                self.tcp_client.send("<donwloadconluido>".encode())
        
            else:
                try:
                    self.tcp_client.send(message.encode())
                except Exception as e:
                    error = "Unable to send message '{}'".format(str(e))
                    print("[INFO]", error)
                    self.show_error("Server Error", error)
                self.chat_ui.msgTextEdit.clear()

    def send_refresh(self):
        try:
            self.tcp_client.send("/refresh".encode())
        except Exception as e:
            error = "Unable to send message '{}'".format(str(e))
            print("[INFO]", error)
            self.show_error("Server Error", error)

    def show_error(self, error_type, message):
        errorDialog = QtWidgets.QMessageBox()
        errorDialog.setText(message)
        errorDialog.setWindowTitle(error_type)
        errorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        errorDialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    c = Client()
    sys.exit(app.exec())