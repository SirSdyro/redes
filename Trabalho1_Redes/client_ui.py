# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(611, 452)
        self.sendButton = QtWidgets.QPushButton(Form)
        self.sendButton.setGeometry(QtCore.QRect(154, 400, 71, 41))
        self.sendButton.setObjectName("sendButton")
        self.messageBrowser = QtWidgets.QTextBrowser(Form)
        self.messageBrowser.setGeometry(QtCore.QRect(20, 40, 341, 271))
        self.messageBrowser.setObjectName("messageBrowser")
        self.msgTextEdit = QtWidgets.QTextEdit(Form)
        self.msgTextEdit.setGeometry(QtCore.QRect(20, 320, 341, 71))
        self.msgTextEdit.setObjectName("msgTextEdit")
        self.groupBrowser = QtWidgets.QTextBrowser(Form)
        self.groupBrowser.setGeometry(QtCore.QRect(380, 150, 211, 71))
        self.groupBrowser.setObjectName("groupBrowser")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(380, 130, 47, 13))
        self.label.setObjectName("label")
        self.canal = QtWidgets.QLabel(Form)
        self.canal.setGeometry(QtCore.QRect(20, 20, 101, 16))
        self.canal.setObjectName("canal")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(380, 240, 141, 16))
        self.label_3.setObjectName("label_3")
        self.serverMsgBrowser = QtWidgets.QTextBrowser(Form)
        self.serverMsgBrowser.setGeometry(QtCore.QRect(380, 260, 211, 131))
        self.serverMsgBrowser.setObjectName("serverMsgBrowser")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(380, 30, 47, 13))
        self.label_4.setObjectName("label_4")
        self.userBrowser = QtWidgets.QTextBrowser(Form)
        self.userBrowser.setGeometry(QtCore.QRect(380, 50, 211, 71))
        self.userBrowser.setObjectName("userBrowser")
        self.refreshButton = QtWidgets.QPushButton(Form)
        self.refreshButton.setGeometry(QtCore.QRect(520, 20, 71, 23))
        self.refreshButton.setObjectName("refreshButton")
        self.clearMsgButton = QtWidgets.QPushButton(Form)
        self.clearMsgButton.setGeometry(QtCore.QRect(290, 10, 71, 23))
        self.clearMsgButton.setObjectName("clearMsgButton")
        self.clearSrvButton = QtWidgets.QPushButton(Form)
        self.clearSrvButton.setGeometry(QtCore.QRect(520, 230, 71, 21))
        self.clearSrvButton.setObjectName("clearSrvButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sendButton.setText(_translate("Form", "Send"))
        self.label.setText(_translate("Form", "Grupos"))
        self.canal.setText(_translate("Form", "Canal: Tela principal"))
        self.label_3.setText(_translate("Form", "Mensagens do servidor"))
        self.label_4.setText(_translate("Form", "Usuários"))
        self.refreshButton.setText(_translate("Form", "Atualizar"))
        self.clearMsgButton.setText(_translate("Form", "Limpar"))
        self.clearSrvButton.setText(_translate("Form", "Limpar"))
