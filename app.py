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
	QAbstractItemView,
	QDialog,
	QMessageBox,
	QCheckBox,
	QSizePolicy
)
from PySide6.QtCore import (
	Qt,
	QAbstractTableModel,
	QRect,
	QTimer
)

class ContactsModel(QAbstractTableModel):
	def __init__(self, contacts=None):
		super().__init__()
		self.contacts = contacts or []
		self.headers = ["First Name", "Last Name", "Phone Number", "Email", "Address"]

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

		self.found_indexes = []
		self.founded_contacts = []

		self.setupUi()

		self.model = ContactsModel()
		self.load()

		self.table_view_contact.setModel(self.model)
		self.table_view_contact.resizeColumnsToContents()

		self.lineedit_search.textChanged.connect(self.search_contact)
		# self.lineedit_search.returnPressed.connect(self.search_contact)

		self.button_add.pressed.connect(self.add_contact)
		self.button_delete.pressed.connect(self.delete_contact)
		self.button_edit.pressed.connect(self.edit_contact)

		self.table_view_contact.doubleClicked.connect(self.edit_contact)
		self.table_view_contact.clicked.connect(lambda: self.button_edit.setDisabled(False))
		self.table_view_contact.clicked.connect(lambda: self.button_delete.setDisabled(False))


	def get_available_coordinates(self):

		geo = self.geometry()

		windowsize = { "x": geo.x(), "y": geo.y(), "width": geo.width(), "height": geo.height()} 

		screensize = { "width": self.screen().size().toTuple()[0], "hieght": self.screen().size().toTuple()[1]}

		dialog_width = 400
		dialog_x = None
		dialog_y = windowsize["y"] + 50

		distance_between_windows = - 200

		if (screensize["width"] - (windowsize["x"] + windowsize["width"]) < (dialog_width + distance_between_windows)):
			dialog_x = windowsize["x"] - (dialog_width + distance_between_windows)

		else:
			dialog_x = windowsize["x"] + windowsize["width"] + distance_between_windows

		return (dialog_x, dialog_y)


	def show_add_contact_dialog(self, existing_contact=None, existing_contact_index=None):

		self.stay_open = False


		dialog = QDialog(self)

		dialog_x , dialog_y = self.get_available_coordinates()

		dialog.setWindowTitle("Add Contact")

		dialog.setModal(True)

		dialog.setFixedWidth(400)
		dialog.setGeometry(dialog_x, dialog_y, 400, 250)

		layout = QVBoxLayout()
		layout.setSpacing(40)
		
		label_add_first_name = QLabel("First Name*")
		label_add_first_name.setFixedWidth(80)
		lineedit_add_first_name = QLineEdit()
		# lineedit_add_first_name.setText(existing_contact[0]) if existing_contact else ""
		if existing_contact:
			lineedit_add_first_name.setText(existing_contact[0])
		lineedit_add_first_name.setPlaceholderText("e.g. Yusuf")
		layout_first_name = QHBoxLayout()
		layout_first_name.addWidget(label_add_first_name)
		layout_first_name.addWidget(lineedit_add_first_name)

		label_add_last_name = QLabel("Last Name*")
		label_add_last_name.setFixedWidth(80)
		lineedit_add_last_name = QLineEdit()
		lineedit_add_last_name.setPlaceholderText("e.g. Totic")
		if existing_contact:
			lineedit_add_last_name.setText(existing_contact[1])
		layout_last_name = QHBoxLayout()
		layout_last_name.addWidget(label_add_last_name)
		layout_last_name.addWidget(lineedit_add_last_name)

		label_add_phone_number = QLabel("Phone Number")
		label_add_phone_number.setFixedWidth(80)
		lineedit_add_phone_number = QLineEdit()
		lineedit_add_phone_number.setPlaceholderText("e.g. +905534762974")
		if existing_contact:
			lineedit_add_phone_number.setText(existing_contact[2])
		layout_phone_number = QHBoxLayout()
		layout_phone_number.addWidget(label_add_phone_number)
		layout_phone_number.addWidget(lineedit_add_phone_number)

		label_add_email = QLabel("Email")
		label_add_email.setFixedWidth(80)
		lineedit_add_email = QLineEdit()
		lineedit_add_email.setPlaceholderText("e.g. yusuftotic@email.com")
		if existing_contact:
			lineedit_add_email.setText(existing_contact[3])
		layout_email = QHBoxLayout()
		layout_email.addWidget(label_add_email)
		layout_email.addWidget(lineedit_add_email)

		label_add_address = QLabel("Address")
		label_add_address.setFixedWidth(80)
		lineedit_add_address = QLineEdit()
		lineedit_add_address.setPlaceholderText("e.g. 202 Elmwood Dr, Mountain Crest, CO 80302")
		if existing_contact:
			lineedit_add_address.setText(existing_contact[4])
		layout_address = QHBoxLayout()
		layout_address.addWidget(label_add_address)
		layout_address.addWidget(lineedit_add_address)


		# form_add_contact = QFormLayout()
		# form_add_contact.setSpacing(15)

		# form_add_contact.addRow(QLabel("First Name*"), lineedit_add_first_name)
		# form_add_contact.addRow(QLabel("Last Name"), lineedit_add_last_name)
		# form_add_contact.addRow(QLabel("Phone Number*"), lineedit_add_phone_number)
		# form_add_contact.addRow(QLabel("Email"), lineedit_add_email)
		# form_add_contact.addRow(QLabel("Address"), lineedit_add_address)
		# layout.addLayout(form_add_contact)


		layout_form = QVBoxLayout()
		layout_form.setSpacing(15)
		layout_form.addLayout(layout_first_name)
		layout_form.addLayout(layout_last_name)
		layout_form.addLayout(layout_phone_number)
		layout_form.addLayout(layout_email)
		layout_form.addLayout(layout_address)

		layout.addLayout(layout_form)


		layout_stay_open = QHBoxLayout()
		layout_stay_open.addStretch()
		label_stay_open = QLabel("Keep window open?")
		layout_stay_open.addWidget(label_stay_open)
		checkbox_stay_open = QCheckBox("Closed")
		layout_stay_open.addWidget(checkbox_stay_open)
		if not existing_contact:
			layout_form.addLayout(layout_stay_open)


		layout_buttons_container = QHBoxLayout()
		layout.addLayout(layout_buttons_container)
		
		button_add = QPushButton("Save Changes" if existing_contact else "Save Contact")
		button_add.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		layout_buttons_container.addWidget(button_add)
		
		button_cancel = QPushButton("Cancel")
		button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		layout_buttons_container.addWidget(button_cancel)

		dialog.setLayout(layout)

		
		def save_contact_data():
			first_name = lineedit_add_first_name.text().strip()
			last_name = lineedit_add_last_name.text().strip()
			phone_number = lineedit_add_phone_number.text().strip()
			email = lineedit_add_email.text().strip()
			address = lineedit_add_address.text().strip()


			if first_name and phone_number:
				
				if existing_contact:
					# index = self.model.contacts.index(existing_contact)
					self.model.contacts[existing_contact_index.row()] = [first_name, last_name, phone_number, email, address]
					self.model.dataChanged.emit(existing_contact_index, existing_contact_index)
					self.table_view_contact.clearFocus()
					self.save()
				else:
					self.model.contacts.append([first_name, last_name, phone_number, email, address])
					self.model.layoutChanged.emit()
					self.save()

				lineedit_add_first_name.clear()
				lineedit_add_last_name.clear()
				lineedit_add_phone_number.clear()
				lineedit_add_email.clear()
				lineedit_add_address.clear()

				if not self.stay_open:
					dialog.close()

				

				lineedit_add_first_name.setFocus()

			else:

				QMessageBox.warning(
					dialog,
					"Add Contact",
					f"Please fill in the required fields",
					QMessageBox.Ok,
					QMessageBox.Ok
				)


		def update_stay_open_state(check_state):
			if check_state == 2: #Qt.CheckState.Checked
				checkbox_stay_open.setText("Open")
				self.stay_open = True

			elif check_state == 0: #Qt.CheckState.Unchecked
				checkbox_stay_open.setText("Closed")
				self.stay_open = False



		lineedit_add_first_name.setFocus()
		lineedit_add_first_name.returnPressed.connect(lambda: lineedit_add_last_name.setFocus())
		lineedit_add_last_name.returnPressed.connect(lambda: lineedit_add_phone_number.setFocus())
		lineedit_add_phone_number.returnPressed.connect(lambda: lineedit_add_email.setFocus())
		lineedit_add_email.returnPressed.connect(lambda: lineedit_add_address.setFocus())
		lineedit_add_address.returnPressed.connect(lambda: button_add.click())
		

		checkbox_stay_open.stateChanged.connect(update_stay_open_state)
		button_add.clicked.connect(save_contact_data)
		button_cancel.clicked.connect(lambda: dialog.close())


		dialog.show()


	def search_contact(self):
		self.load()
		search_text = self.lineedit_search.text().strip().lower()

		contacts = self.model.contacts

		# QTimer.singleShot(300, lambda: print(search_text))

		self.found_indexes.clear()
		self.founded_contacts.clear()

		# QTimer.singleShot(300, lambda: self.linear_search(contacts, search_text))
		self.linear_search(self.model.contacts, search_text)

		print(self.found_indexes)
		
		if len(search_text) == 0:
			self.load()
			self.model.layoutChanged.emit()
			return

		if len(self.found_indexes) > 0:
			self.founded_contacts = [contacts[i] for i in self.found_indexes]
			self.model.contacts = self.founded_contacts
			self.model.layoutChanged.emit()
		else:
			self.load()
			self.model.layoutChanged.emit()


	def linear_search(self, data, target):
		for i in range(len(data)):
			for j in range(len(data[0])):
				if target in data[i][j].lower():
					if i in self.found_indexes:
						continue
					self.found_indexes.append(data.index(data[i]))

		if len(self.found_indexes) > 0:
			return self.found_indexes
		else:
			return -1



	def add_contact(self):
		self.show_add_contact_dialog()


	def delete_contact(self):

		indexes = self.table_view_contact.selectedIndexes()
		
		contact = self.model.contacts[indexes[0].row()]

		if indexes:
			reply = QMessageBox.question(
				self,
				"Delete Contact",
				f"Are you sure you want to delete {contact[0]} {contact[1]} contact?",
				QMessageBox.Yes | QMessageBox.No,
				QMessageBox.No
			)

			if reply == QMessageBox.Yes:
				del self.model.contacts[indexes[0].row()]
				self.model.layoutChanged.emit()
				self.table_view_contact.clearSelection()
				self.button_delete.setDisabled(True)
				self.button_edit.setDisabled(True)
				self.save()
			else:
				self.table_view_contact.clearSelection()



	def edit_contact(self):
		indexes = self.table_view_contact.selectedIndexes()
		if indexes:
			row = indexes[0].row()
			contact = self.model.contacts[row]
			# print(self.model.contacts)
			self.show_add_contact_dialog(contact, indexes[0])


	def load(self):
		try:
			with open(ContactsApp.csv_path, "r", encoding="utf-8", newline="") as csvfile:
				
				reader = csv.reader(csvfile, delimiter=",")

				headers = next(reader)

				self.model.contacts = list(reader)


		except Exception:
			pass

	
	def save(self):
		with open(ContactsApp.csv_path, "w", encoding="utf-8", newline="") as csvfile:

			writer = csv.writer(csvfile, delimiter=",")

			writer.writerow(self.model.headers)
			writer.writerows(self.model.contacts)

	def setupUi(self):

		self.setWindowTitle("Contacts App")
		self.setFixedSize(700, 500)
		# self.resize(500, 400)
		# self.setMinimumSize(500, 400)
		# self.setMaximumSize(700, 500)

		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		layout = QVBoxLayout()
		# layout.setSpacing(20)
		central_widget.setLayout(layout)

		layout_search = QHBoxLayout()
		self.lineedit_search = QLineEdit()
		self.lineedit_search.setPlaceholderText("Search")
		self.lineedit_search.setFixedWidth(400)
		self.lineedit_search.setFixedHeight(25)
		layout_search.addWidget(self.lineedit_search)
		layout.addLayout(layout_search)

		label_table_view = QLabel("Contacts")
		label_table_view.setStyleSheet("font-size: 20px; margin-top:15px")
		self.table_view_contact = QTableView()
		self.table_view_contact.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.table_view_contact.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.table_view_contact.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
		self.table_view_contact.setMinimumHeight(300)
		layout.addWidget(label_table_view)
		layout.addWidget(self.table_view_contact)


		layout_buttons_container = QHBoxLayout()
		layout.addLayout(layout_buttons_container)
		
		self.button_add = QPushButton("Add Contact")
		layout_buttons_container.addWidget(self.button_add)

		self.button_edit = QPushButton("Edit")
		self.button_edit.setDisabled(True)
		layout_buttons_container.addWidget(self.button_edit)

		self.button_delete = QPushButton("Delete")
		self.button_delete.setDisabled(True)
		layout_buttons_container.addWidget(self.button_delete)

		# layout.addStretch()

	



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = ContactsApp()
	window.show()
	sys.exit(app.exec())
