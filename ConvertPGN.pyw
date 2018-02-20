# -*- coding: latin-1 -*-
#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name:        ConvertPGN.pyw
# Purpose:
#
# Author:      rapapla
# Created:     05/10/2015
# Copyright:   (c) rapapla 2015
# Licence:     <vide sidérale>
#-------------------------------------------------------------------------------

import os
import platform
import stat
import sys
import glob
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = "0.1"
extension = ".pgn"

class OptionsForm(QDialog):

    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)

class Form(QMainWindow):

    def __init__(self):
        super(Form, self).__init__(None)

        pathLabel = QLabel("Path:")
        path = os.getcwd()
        self.pathLabel = QLabel(path)
        self.pathLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.pathLabel.setToolTip("The relative path; all actions will take place here")
        self.pathButton = QPushButton("&Path...")
        self.pathButton.setToolTip(self.pathLabel.toolTip().replace("The", "Sets the"))
        self.logBrowser = QTextBrowser()
        self.logBrowser.setLineWrapMode(QTextEdit.NoWrap)
        self.buttonBox = QDialogButtonBox()
        menu = QMenu(self)
        optionsAction = menu.addAction("&Options...")
        aboutAction = menu.addAction("&About")
        moreButton = self.buttonBox.addButton("&More", QDialogButtonBox.ActionRole)
        moreButton.setMenu(menu)
        self.mergeButton = self.buttonBox.addButton("&Merge", QDialogButtonBox.ActionRole)
        self.mergeButton.setToolTip("merge all *.pgn files ")
        quitButton = self.buttonBox.addButton("&Quit", QDialogButtonBox.RejectRole)

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)
        topLayout.addWidget(self.pathButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.buttonBox)
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.logBrowser)
        layout.addLayout(bottomLayout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.connect(aboutAction, SIGNAL("triggered()"), self.about)
        self.connect(optionsAction, SIGNAL("triggered()"), self.setOptions)
        self.connect(self.pathButton, SIGNAL("clicked()"), self.setPath)
        # -- ToDo --
        # afficher le contenu du repertoire initial
        self.connect(self.pathButton, SIGNAL("triggered()"), self.setPath)
        self.connect(self.mergeButton, SIGNAL("clicked()"), self.merge)
        self.connect(quitButton, SIGNAL("clicked()"), self.close)

        self.setWindowTitle("Merge PGN")

    def closeEvent(self, event):
        pass

    def about(self):
        QMessageBox.about(self, "About Merge PGN",
                """<b>Merge PGN</b> - v {0}
                <p>Copyright &copy; Games Factory.
                All rights reserved.
                <p>This application is used to merge
                multiples pgn files to one pgn file
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))

    def setPath(self):
        path = QFileDialog.getExistingDirectory(self, "Merge PGN - Set Path", self.pathLabel.text())
        if path:
            self.pathLabel.setText(QDir.toNativeSeparators(path))
        #names = os.listdir(path)
        names = glob.glob(path +'\\*' + extension)
        for nom in names:
            self.logBrowser.append(nom)

    def setOptions(self):
        dlg = OptionsForm(self)
        dlg.exec_()

    def merge(self):
        path = self.pathLabel.text()
        liste_fichier = self.logBrowser.toPlainText().split("\\r")
        if len(liste_fichier)>1:
            with open(path + '\\TOUT'+extension, 'a') as grand:
                for nom_de_fichier in self.logBrowser.toPlainText().split("\n"):
                    with open(nom_de_fichier, 'r') as petit:
                        partie = petit.read()
                        grand.write(partie + "\n\n")
        self.logBrowser.append(u"\n\n------------------\nTerminée")

    def clean(self):
        pass

    def updateUi(self, enable):
        for widget in (self.mergeButton, self.cleanButton, self.pathButton):
            widget.setEnabled(enable)
        if not enable:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        else:
            QApplication.restoreOverrideCursor()
            self.mergeButton.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.resize(400,300)
    form.show()
    app.exec_()
