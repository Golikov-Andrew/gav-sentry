import csv
import os
from datetime import datetime


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


if __name__ == '__main__':
	sentry = Sentry()
	cur_dir = os.path.abspath(os.curdir)
	grafic_file_path = os.path.join(cur_dir, 'shedules', 'grafic_2.csv')
	interval_min = 15
	sentry.generate_shedule(grafic_file_path, interval_min)

# now = datetime(2020,11,16)
# print(now.weekday())
