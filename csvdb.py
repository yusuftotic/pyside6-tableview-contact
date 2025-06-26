import csv
import os
import uuid

class CSVDB:

	current_folder_path = os.path.dirname(os.path.abspath(__file__))


	HEADERS = ["ID", "First Name", "Last Name", "Phone Number", "Email", "Address"]
	

	def __init__(self, file_name:str):
		self.csv_file_path = os.path.join(CSVDB.current_folder_path, f"{file_name}.csv")
		
		if not self.is_file_exist():
			self.create_csv_file()


	def is_file_exist(self):
		return os.path.exists(self.csv_file_path)

	def create_csv_file(self):
		with open(self.csv_file_path, "w", encoding="utf-8", newline="") as csvfile:
			writer = csv.writer(csvfile)
			
			writer.writerow(CSVDB.HEADERS)

			print("[INFO] - contacts.csv created successfully.")

	def create(self, data:list):

		_id = uuid.uuid4()
		_id_hex = _id.hex
		
		with open(self.csv_file_path, "a", encoding="utf-8", newline="") as csvfile:
			
			writer = csv.writer(csvfile, delimiter=",")

			data.insert(0, _id_hex)

			writer.writerow(data)


	def find_all(self):
		with open(self.csv_file_path, "r", encoding="utf-8", newline="") as csvfile:

			reader = csv.reader(csvfile)

			headers = next(reader)

			data = list(reader)

			return data
	
	def find(self, target):
		data = self.find_all()
		found_contacts = []
		for i in range(len(data)):
			for j in range(len(data[0])):
				if target in data[i][j].lower():
					if data[i] in found_contacts:
						continue
					found_contacts.append(data[i])

		if len(found_contacts) > 0:
			return found_contacts
		else:
			return -1

	def find_by_id(self, _id:str):
		
		with open(self.csv_file_path, "r", encoding="utf-8", newline="") as csvfile:

			reader = csv.reader(csvfile)

			headers = next(reader)

			data = list(reader)

			person = None
			for row in data:
				if row[0] == _id:
					person = row

			return person

	def edit(self, _id:str, new_data:list):

		all_data = self.find_all()

		for i, row in enumerate(all_data):
			if row and row[0] == _id:
				new_data.insert(0, _id)
				
				all_data.pop(i)
				all_data.insert(i, new_data)


		self._write_all_records(all_data)


	def delete_by_id(self, _id:str):
		record = self.find_by_id(_id)

		if not record:
			return

		all_records = self.find_all()

		record_index = all_records.index(record)

		all_records.pop(record_index)

		self._write_all_records(all_records)


	def _write_all_records(self, records):
		with open(self.csv_file_path, "w", encoding="utf-8", newline="") as csvfile:
			writer = csv.writer(csvfile, delimiter=",")
			writer.writerow(CSVDB.HEADERS)
			writer.writerows(records)
