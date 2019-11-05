import os
import shutil
import datetime
import re
import json
import sys


try:
	with open('settings.json', 'r') as read_file:
		settings = json.load(read_file)
except:
	input('Не найден settings.json. Нажмите Enter')
	sys.exit()

path_out = settings['path']['from']
path_in = settings['path']['to']

if os.path.exists(path_in):
	shutil.rmtree(path_in)

today = datetime.datetime.today()
path_in = os.path.join(path_in, 'Схемы от ' + today.strftime('%d-%m-%y_%H-%M'))

os.makedirs(os.path.join(path_in, 'ВЛ-0,4кВ'))
os.makedirs(os.path.join(path_in, 'ВЛ,КЛ-10кВ'))
os.makedirs(os.path.join(path_in, 'ТП,КТП,МТП'))

try:
	files = os.listdir(path_out)
except:
	input('Не найден путь {}. Нажми Enter'.format(path_out))
vsd_files = filter(lambda x: x.endswith('.vsd') and ('50565202' in x), files)

i = 0
errorfiles = []

for file in vsd_files:
	if 'CL038' in file:
		new_name = re.search(r'-(\d+)_', file)[0]
		new_name = re.search(r'\d+', new_name)[0] + '.vsd'
		path_for_save = os.path.join(path_in, 'ВЛ-0,4кВ')
	elif 'VL10' in file:
		new_name = 'ВЛ-' + file.split('-')[-1]
		path_for_save = os.path.join(path_in, 'ВЛ,КЛ-10кВ')
	elif 'CL10' in file:
		new_name = 'КЛ-' + file.split('-')[-1]
		path_for_save = os.path.join(path_in, 'ВЛ,КЛ-10кВ')
	elif 'TP' in file or 'RP' in file:
		new_name = file.split('-')[-1]
		path_for_save = os.path.join(path_in, 'ТП,КТП,МТП')
	else:
		errorfiles.append(file)
		continue

	shutil.copyfile(os.path.join(path_out, file), os.path.join(path_for_save, new_name))
	print(file)
	i = i + 1

print('Переименовано {} схем'.format(i))
if errorfiles:
	print ('Файлы не прошедшие отбор: ', errorfiles)
input('Press Enter')
