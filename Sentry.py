import time
import csv
import os
from datetime import datetime
from FromCsvToListOfDictLoader import FromCsvToListOfDictLoader as CsvReader


class Sentry:
	def __init__(self):
		pass

	def generate_shedule(self, dest_file_path, interval_min):
		header = ['is_enabled', 'minute', 'hour', 'day_of_week']
		data = list()
		data.append(header)

		min = 0
		hour = 0
		dow = 0

		while True:
			data.append([1, min, hour, dow + 1])
			min += interval_min
			dif = 60 - min
			if dif <= 0:
				min = -dif
				hour += 1
				dif_h = 24 - hour
				if dif_h <= 0:
					hour = -dif_h
					dow += 1
					dif_dow = 7 - dow
					if dif_dow <= 0:
						break

		with open(dest_file_path, 'w', encoding='utf-8') as f:
			csv_writer = csv.writer(f, delimiter=';')
			for row in data:
				csv_writer.writerow(row)

	def set_shedule(self, grafic_file_path):
		self.shedule_dict = dict()
		csv_reader = CsvReader()
		data_from_csv = csv_reader.read(grafic_file_path)
		for entity in data_from_csv:
			if entity['is_enabled'] == '1':
				min = entity['minute']
				if not min in self.shedule_dict:
					self.shedule_dict[min] = dict()
				hour = entity['hour']
				if not hour in self.shedule_dict[min]:
					self.shedule_dict[min][hour] = dict()
				dow = entity['day_of_week']
				if not dow in self.shedule_dict[min][hour]:
					self.shedule_dict[min][hour][dow] = dict()


	def check_now(self):
		min = str(datetime.now().minute)
		hour = str(datetime.now().hour)
		dow = str(datetime.now().weekday())
		if min in self.shedule_dict:
			if hour in self.shedule_dict[min]:
				if dow in self.shedule_dict[min][hour]:
					return True
		return False

	def run(self, func, interval_check):
		while True:
			print("\r%s Waiting..." % datetime.now(), end="")
			if self.check_now():
				print()
				func()
			time.sleep(interval_check * 60)

if __name__ == '__main__':
	sentry = Sentry()
	cur_dir = os.path.abspath(os.curdir)
	grafic_file_path = os.path.join(cur_dir, 'shedules', 'grafic.csv')


	# interval_min = 15
	# sentry.generate_shedule(grafic_file_path, interval_min)

	def func():
		print("%s test" % datetime.now())

	sentry.set_shedule(grafic_file_path)
	sentry.run(func, 1)

