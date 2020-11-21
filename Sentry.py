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
		min_per_day = 1440
		init_min = 0
		init_hour = 0
		hours = min_per_day / interval_min
		for dow in range(7):
			for h in range(int(hours)):
				data.append([1, init_min, init_hour, dow + 1])
				init_min += interval_min
				dif = 60 - init_min
				if dif <= 0:
					init_min = -dif
					init_hour += 1
					dif_h = 24 - init_hour
					if dif_h <= 0:
						init_hour = -dif_h

		with open(dest_file_path, 'w', encoding='utf-8') as f:
			csv_writer = csv.writer(f, delimiter=';')
			for row in data:
				csv_writer.writerow(row)


if __name__ == '__main__':
	sentry = Sentry()
	cur_dir = os.path.abspath(os.curdir)
	grafic_file_path = os.path.join(cur_dir, 'shedules', 'grafic.csv')
	interval_min = 15
	sentry.generate_shedule(grafic_file_path, interval_min)

# now = datetime(2020,11,16)
# print(now.weekday())
