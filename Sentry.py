import time
import csv
import os
from datetime import datetime
from FromCsvToListOfDictLoader import FromCsvToListOfDictLoader as CsvReader


class Sentry:
	def __init__(self):
		pass

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

	def generate_shedule(self, grafic_file_path, interval_min, begin_date, end_date):
		header = ['is_enabled', 'minute', 'hour', 'day_of_week']
		data = list()
		data.append(header)

		delta_sec = interval_min * 60
		begin_datetime = datetime.strptime(begin_date, '%Y-%m-%d %H:%M')
		end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
		begin_timestamp = begin_datetime.timestamp()
		end_timestamp = end_datetime.timestamp()

		cur_timestamp = begin_timestamp
		while cur_timestamp < end_timestamp:
			datetime_obj = datetime.fromtimestamp(cur_timestamp)
			print(datetime_obj)
			min = datetime_obj.minute
			hour = datetime_obj.hour
			dow = datetime_obj.weekday()
			data.append([1, min, hour, dow + 1])
			cur_timestamp += delta_sec

		with open(grafic_file_path, 'w', encoding='utf-8') as f:
			csv_writer = csv.writer(f, delimiter=';')
			for row in data:
				csv_writer.writerow(row)


if __name__ == '__main__':
	sentry = Sentry()
	cur_dir = os.path.abspath(os.curdir)
	grafic_file_path = os.path.join(cur_dir, 'shedules', 'grafic_2.csv')

	interval_min = 15
	sentry.generate_shedule(grafic_file_path, interval_min, '2020-11-23 00:00', '2020-11-30 00:00')

	def func():
		print("%s test" % datetime.now())

	sentry.set_shedule(grafic_file_path)
	sentry.run(func, 1)
