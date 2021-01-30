from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os
import sys

class MainWindow(QMainWindow):

	def __init__(self, *args, **kwargs):
		super(MainWindow,self).__init__(*args, **kwargs)

		layout = QVBoxLayout()

		self.editor = QPlainTextEdit()
		

		fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
		fixedfont.setPointSize(12)
		self.editor.setFont(fixedfont)


		self.path = None

		layout.addWidget(self.editor)


		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)


		self.status = QStatusBar()
		self.setStatusBar(self.status)




		file_toolbar = QToolBar("File")
		file_toolbar.setIconSize(QSize(14,14))
		self.addToolBar(file_toolbar)
		file_menu = self.menuBar().addMenu("&File")




		open_action = QAction(QIcon(os.path.join('images','blue-folder-open-document.png')),"Open file....",self)
		open_action.setStatusTip("Open file")
		open_action.triggered.connect(self.file_open)
		file_menu.addAction(open_action)
		file_toolbar.addAction(open_action)



		save_action = QAction(QIcon(os.path.join('images','disk.png')),"Save",self)
		save_action.setStatusTip("Save current page")
		save_action.triggered.connect(self.file_save)
		file_menu.addAction(save_action)
		file_toolbar.addAction(save_action)
		



		saveas_action = QAction(QIcon(os.path.join('images','disk--pencil.png')),"Save As.......",self)
		saveas_action.setStatusTip("Save current page to specified file")
		saveas_action.triggered.connect(self.file_saveas)
		file_menu.addAction(saveas_action)
		file_toolbar.addAction(saveas_action)
		






		edit_toolbar = QToolBar("Edit")
		edit_toolbar.setIconSize(QSize(16,16))
		self.addToolBar(edit_toolbar)
		edit_menu = self.menuBar().addMenu("&Edit")



		cut_action = QAction(QIcon(os.path.join('images','scissors.png')),"Cut",self)
		cut_action.setStatusTip("Copy selected text")
		cut_action.triggered.connect(self.editor.cut)
		edit_toolbar.addAction(cut_action)
		edit_menu.addAction(cut_action)


		copy_action = QAction(QIcon(os.path.join('images','document-copy.png')),"Copy",self)
		copy_action.setStatusTip("Cut selected text")
		copy_action.triggered.connect(self.editor.copy)
		edit_toolbar.addAction(copy_action)
		edit_menu.addAction(copy_action)


		paste_action = QAction(QIcon(os.path.join('images','clipboard-paste-document-text.png')),"Paste",self)
		paste_action.setStatusTip("Paste from clipboard")
		paste_action.triggered.connect(self.editor.paste)
		edit_toolbar.addAction(paste_action)
		edit_menu.addAction(paste_action)


		select_action = QAction(QIcon(os.path.join('images','selection-input.png')),"Select",self)
		select_action.setStatusTip("Select all text")
		select_action.triggered.connect(self.editor.selectAll)
		edit_toolbar.addAction(select_action)
		edit_menu.addAction(select_action)



		edit_menu.addSeparator()


		tab_action = QAction(QIcon(os.path.join('images','ui-tab--plus.png')),"New File",self)
		tab_action.setStatusTip("Select all text")
		tab_action.triggered.connect(self.editor.selectAll)
		edit_toolbar.addAction(tab_action)
		edit_menu.addAction(tab_action)


		

		self.update_title()
		self.show()


	def dialog_critical(self ,s):
		dlg = QMessageBox(self)
		dlg.setText(s)
		dlg.setIcon(QMessageBox.Critical)
		dlg.show()



	def file_open(self):

		path,_ =QFileDialog.getOpenFileName(self,"Open File","","Text Documents (*.txt); All Files (*.*)")

		if path:
			try:
				with open(path,'rU') as f:
					text = f.read()

			except Exception as e:
				self.dialog_critical(str(e))

			else:
				self.path = path
				self.editor.setPlainText(text)
				self.update_title()



	def file_save(self):
		if self.path is None:
			return self.file_saveas()


		self.save_topath(self.path)


	def file_saveas(self):
		path,_ = QFileDialog.getSaveFileName(self,"Save FIle","","Text Documents (*.txt); All Files (*.*)")

		if not path:
			return

		self.save_topath(self,path)


	def sae_topath(self,path):
		text = self.editor.toPlainText()
		try:
			with open(path,'w') as f:
				f.write(text)
		except Exception as e:
			self.dialog_critical(str(e))
		else:
			self.path = path
			self.update_title()





	def update_title(self):
		self.setWindowTitle("%s-!aTxtEditor"%(os.path.basename(self.path) if self.path else "Untitled"))



if __name__ == '__main__':
	app = QApplication(sys.argv)

	app.setApplicationName("!aTxtEditor")

	window = MainWindow()

	app.exec_()