import sys
import os
import csv
from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QFormLayout,
	QLineEdit,
	QLabel,
	QPushButton,
	QTableView,
	QAbstractItemView
)
from PySide6.QtCore import (
	Qt,
	QAbstractTableModel,
)

class ContactsModel(QAbstractTableModel):
	def __init__(self, contacts=None):
		super().__init__()
		self.contacts = contacts or []
		self.headers = ["First Name", "Last Name", "Phone Number", "Email", "Adress"]

	def data(self, index, role):

		if not index.isValid():
			return None

		if role == Qt.ItemDataRole.DisplayRole:

			return self.contacts[index.row()][index.column()]
		
	def rowCount(self, index):
		return len(self.contacts)
	
	def columnCount(self, index):
		return len(self.headers)
	
	# Table View Header Ayarlama
	def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
		if role == Qt.ItemDataRole.DisplayRole:
			if orientation == Qt.Orientation.Horizontal:
				return self.headers[section]
			elif orientation == Qt.Vertical:
				return str(section + 1)


class ContactsApp(QMainWindow):

	current_file_path = os.path.abspath(__file__)
	current_folder_path = os.path.dirname(current_file_path)
	csv_path = os.path.join(current_folder_path, "data.csv")	

	def __init__(self):
		super().__init__()

		self.setupUi()

		self.model = ContactsModel()
		self.load()

		self.table_view_contact.setModel(self.model)


		self.button_add.pressed.connect(self.add_contact)
		self.button_delete.pressed.connect(self.delete_contact)
		self.button_edit.pressed.connect(self.edit_contact)
		self.table_view_contact.doubleClicked.connect(self.edit_contact)




	def add_contact(self):
		first_name = self.lineedit_add_first_name.text().strip()
		last_name = self.lineedit_add_last_name.text().strip()
		phone_number = self.lineedit_add_phone_number.text().strip()
		email = self.lineedit_add_email.text().strip()
		adress = self.lineedit_add_adress.text().strip()


		if first_name and phone_number:
			self.model.contacts.append([first_name, last_name, phone_number, email, adress])
			self.model.layoutChanged.emit()

			self.save()

			self.lineedit_add_first_name.clear()
			self.lineedit_add_last_name.clear()
			self.lineedit_add_phone_number.clear()
			self.lineedit_add_email.clear()
			self.lineedit_add_adress.clear()

		else:
			print("Zorunlu alanları doldur.")




	def delete_contact(self):

		indexes = self.table_view_contact.selectedIndexes()

		if indexes:
			del self.model.contacts[indexes[0].row()]
			self.model.layoutChanged.emit()

			self.table_view_contact.clearSelection()

			self.save()



	def edit_contact(self):
		pass


	def load(self):
		try:
			with open(ContactsApp.csv_path, "r", encoding="utf-8", newline="") as csvfile:
				
				reader = csv.reader(csvfile)

				headers = next(reader)

				self.model.contacts = list(reader)


		except Exception:
			pass

	
	def save(self):
		with open(ContactsApp.csv_path, "w", encoding="utf-8", newline="") as csvfile:

			writer = csv.writer(csvfile)

			writer.writerow(self.model.headers)
			writer.writerows(self.model.contacts)

	def setupUi(self):

		self.setWindowTitle("Contact")
		# self.setFixedSize(600, 500)
		self.setFixedWidth(600)

		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		layout = QVBoxLayout()
		# layout.setSpacing(20)
		central_widget.setLayout(layout)

		self.label_add_first_name = QLabel("First Name")
		self.lineedit_add_first_name = QLineEdit()
		self.lineedit_add_first_name.setPlaceholderText("e.g. Yusuf")

		self.label_add_last_name = QLabel("Last Name")
		self.lineedit_add_last_name = QLineEdit()
		self.lineedit_add_last_name.setPlaceholderText("e.g. Totic")

		self.label_add_phone_number = QLabel("Phone Number")
		self.lineedit_add_phone_number = QLineEdit()
		self.lineedit_add_phone_number.setPlaceholderText("e.g. +905534762974")

		self.label_add_email = QLabel("Email")
		self.lineedit_add_email = QLineEdit()
		self.lineedit_add_email.setPlaceholderText("e.g. yusuftotic@email.com")

		self.label_add_adress = QLabel("Adress")
		self.lineedit_add_adress = QLineEdit()
		self.lineedit_add_adress.setPlaceholderText("e.g. 202 Elmwood Dr, Mountain Crest, CO 80302")

		form_add_contact = QFormLayout()
		form_add_contact.setSpacing(15)

		form_add_contact.addRow(QLabel("First Name*"), self.lineedit_add_first_name)
		form_add_contact.addRow(QLabel("Last Name"), self.lineedit_add_last_name)
		form_add_contact.addRow(QLabel("Phone Number*"), self.lineedit_add_phone_number)
		form_add_contact.addRow(QLabel("Email"), self.lineedit_add_email)
		form_add_contact.addRow(QLabel("Adress"), self.lineedit_add_adress)

		layout.addLayout(form_add_contact)
		
		self.button_add = QPushButton("Add Contact")
		layout.addWidget(self.button_add)

		label_table_view = QLabel("Contact")
		label_table_view.setStyleSheet("font-size: 15px; margin-top:15px")
		self.table_view_contact = QTableView()
		self.table_view_contact.resizeColumnsToContents() # BU NE İŞE YARIYOR?????
		self.table_view_contact.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.table_view_contact.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
		self.table_view_contact.setMinimumHeight(300)
		layout.addWidget(label_table_view)
		layout.addWidget(self.table_view_contact)


		layout_buttons_container = QHBoxLayout()
		layout.addLayout(layout_buttons_container)

		self.button_delete = QPushButton("Delete")
		layout_buttons_container.addWidget(self.button_delete)

		self.button_edit = QPushButton("Edit")
		layout_buttons_container.addWidget(self.button_edit)

		layout.addStretch()

	



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = ContactsApp()
	window.show()
	sys.exit(app.exec())
