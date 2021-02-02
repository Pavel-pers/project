import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import random
import datetime

# ВЫВОД ВСЕХ ДНЕЙ В ГРАФИКЕ 
def all_tm():
	# ПОДКЛЮЧЕНИЕ 
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	# МАССИВЫ ОСЕЙ
	mathx = []
	mathy = []
	engy = []

	# ЦИКЛ ПО ВСЕМ ДНЕЙ ГДЕ ПРОИСХОДИЛИ КАКИЕ-ТО ДЕЙСТВИЯ (ЗАМЕНА ЕХР ИЛИ ЗАМЕНА КОЛЛ НЕПРАВИЛЬНЫХ ОТВЕТОВ)В КАКОМ ЛИБО ПРЕДМЕТЕ 
	tt1 = 0
	for ii in sql.execute("SELECT * FROM user"):
		db = sqlite3.connect('server.db')  
		sql = db.cursor()

		# ДОБАВЛЕНИЕ ТАКОЙ ТОЧКИ Х НА ГРАФИКЕ
		'''
	dt TEXT, - ii[0] - ДАТА
	exp INTEGER, - ii[1] - КОЛЛ ЕХР
	subject TEXT, - ii[2] - НАЗВАНИЕ ПРЕДМЕТА
	A INTEGER, - ii[3] КОЛЛ ПР ОТВЕТОВ
	F INTEGER - ii[4] КОЛЛ НЕ ПРАВИЛЬНЫХ ОТВЕТОВ 


		'''
		if tt1 > 5:
			mathx.append(ii[0])
			# ПОИСК ДАТЫ ПО КОТОТОРОЙ ИДЕМ ЦИКЛОМ + ТАМ ГДЕ ПРЕДМЕТ МАТЕМАТИКА
			sql.execute(f"SELECT * FROM user WHERE dt = '{ii[0]}' and subject = 'math'")
			ff1 = sql.fetchone()
			# НАШЛАСЬ СТРОКА 
			if ff1 != None:
				mathy.append(ff1[1])
			# НЕ НАШЛАСЬ СТРОКА ГДЕ БЫЛИ ИЗМЕНЕНИЯ ЕХР - ПОЛУЧАЕТСЯ ЕХР РАВНО НУЛЮ В ЭТОТ ДЕНЬ
			else:
				mathy.append(0)
			
			# ПОИСК ДАТЫ ПО КОТОТОРОЙ ИДЕМ ЦИКЛОМ + ТАМ ГДЕ ПРЕДМЕТ АНГЛИЙСКИЙ		
			sql.execute(f"SELECT * FROM user WHERE dt = '{ii[0]}' and subject = 'eng'")
			ff2 = sql.fetchone()

			# НАШЛАСЬ СТРОКА 
			if ff2 != None:
				engy.append(ff2[1])
			# НЕ НАШЛАСЬ СТРОКА ГДЕ БЫЛИ ИЗМЕНЕНИЯ ЕХР - ПОЛУЧАЕТСЯ ЕХР РАВНО НУЛЮ В ЭТОТ ДЕНЬ
			else:
				engy.append(0)
		else:
			tt1+=1

	# КОРДИНАТЫ Х
	x_ind = np.arange(len(mathx))
	wh = 0.4
	#ПОСТРОЕНИЕ ГРАФИКА
	plt.xlabel('days')
	plt.ylabel('EXP')

	plt.xticks(x_ind, mathx)

	# 1 ПАРАМЕТРЫ КОРДИНАТЫ , СДВИГАЮ ПЕРВЫЙ СТОЛБЕЦ(МАТЕМАТИКУ) НА ЛЕВО А ВТОРОЙ НА ПРАВА
	plt.bar(x_ind - (wh / 2), mathy, label = ('math'), width = wh)
	plt.bar(x_ind + (wh / 2), engy, label = ('eng'), width = wh)

	plt.legend()
	plt.show()

def diff(sb):
	#ПОДКЛЮЧЕНИЕ 
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	xx = []
	ty = []
	fy = []
	#ПРОСМОТР СТРОКИ С ПРЕДМЕТОМ ИЗ ФУНКЦИИ  
	for ii in sql.execute(f"SELECT * FROM user WHERE subject = '{sb}'"):
		xx.append(ii[0])
		ty.append(ii[3])
		fy.append(ii[4])

	x_ind = np.arange(len(xx))
	wh = 0.4

	# ПОСТРОЕНИЕ ГРАФИКА СЛЕВА СДВИГАЮ ПРАВИЛЬНЫЕ ОТВЕТЫ, СПРАВА НЕ ПРАВИЛЬНЫЕ
	plt.xticks(x_ind, xx)

	plt.bar(x_ind - (wh / 2), ty, label = ("True answer"), width = wh, color = 'g')	
	plt.bar(x_ind + (wh / 2), fy, label = ("Wrong answer"), width = wh, color = 'r')

	plt.legend()
	plt.show()
