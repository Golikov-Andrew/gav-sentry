import csv


class FromCsvToListOfDictLoader:
	def __init__(self):
		pass

	def read(self, filepath) -> list:
		data = list()
		headers = list()
		count_cell_in_row = 0
		with open(filepath, 'r', encoding='utf-8') as f:
			csv_reader = csv.reader(f, delimiter=';')
			for line in csv_reader:
				if csv_reader.line_num == 1:
					for head in line:
						headers.append(head)
						count_cell_in_row += 1
				else:
					cur_item = dict()
					cur_cell_idx = 0
					for cell in line:
						cur_key = headers[cur_cell_idx]
						cur_item[cur_key] = cell
						cur_cell_idx += 1
					data.append(cur_item)
					# print(cur_item)
		return data
