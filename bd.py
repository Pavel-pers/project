# РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ 
import re
# РАНДОМ ИСПОЛЬЗУЕТСЯ ДЛЯ ЗАМЕНЫ ПЕРЕМЕННЫХ КАК &1 НА РАНДОМНЫЕ ЧИСЛА
import random
# МОДУЛЬ БАЗЫ ДАННЫХ
import sqlite3
# МОДУЛЬ ДЛЯ РАБОТЫ С ДАТАМИ 
import datetime
# МОДУЛЬ ДЛЯ ОЧИЩЕНИЯ CMD
import os
# СВОЙ МОДУЛЬ ДЛЯ УПРАВЛЕНИЯ БАЗЫ ДЫННЫХ
import pp
# СВОЙ МОДУЛЬ ДЛЯ ВЫВОДА СТАТИСТИКИ
import statistic


# ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
db = sqlite3.connect('server.db')  
sql = db.cursor()

# ВЫБОР ПРЕДМЕТА
subj = input('выберите предмет - ')

while 1:
	#ВЫБОР РАНДОМНОЙ СТРОКИ ИЗ БД ГДЕ subject = ВВЕДЕННЫМ ПОЛЬЗОВАТЕЛЕМ  ПРЕДМЕТОМ
	sql.execute(f"SELECT * FROM questions WHERE subject = '{subj}' ORDER BY RANDOM() LIMIT 1;")
	data = sql.fetchone()
	# ОПРЕДЕЛЕНИЕ СЕГОДЕШНЕГО ДНЯ дд-мм-гггг
	# now = datetime.datetime.now()
	# now = now.strftime(f"%d-%m-%Y")
	now = input()

	# ИЗМЕНЕНИЕ ПЕРЕМЕННЫХ В ОТВЕТЕ+В ВОПРОСЕ
	qn = data[0]
	ans = data[1]	
	q = []
	# Q1 И Q- МАССИВ ПАР ЧИСЕЛ КОТОРЫЕ ДЕЛЯТСЯ В ВЫРАЖЕНИЕ 
	q1 = re.findall(r"(&?\d+)/(&?\d+)", ans)
	q = []
	for i in q1:
		q.append([i[0], i[1]])
	
	# ЗАМЕНА ЧИСЕЛ ТАК ЧТО БЫ ОНИ ДЕЛИЛИСЬ ПОРОВНУ
	for i in range(len(q)):
		q[i][0] = re.sub('<', '', str(q[i][0]))
		q[i][1] = re.sub('<', '', str(q[i][1]))
		q[i][0] = re.sub('>', '', str(q[i][0]))
		q[i][1] = re.sub('>', '', str(q[i][1]))
		try:
			# ВТОРОЕ ЧИСЛО ИЗВЕСТНО, ПЕРВОЕ НЕ ИЗВЕСТНО
			rnd1 = random.randint(1, 20)
			ans = re.sub(q[i][0], str(int(q[i][1]) * rnd1), ans)
			qn = re.sub(q[i][0], str(int(q[i][1]) * rnd1), qn)
		except:
			# ВТОРОЕ ЧИСДО НЕ ИЗВЕСТНО
			try:
				# ПЕРВОЕ ЧИСЛО ИЗВЕСТНО 
				dd = []
				ii1 = 1
				while ii1 <= int(q[i][0]):
					if (int(q[i][0]) % ii1) == 0:
						dd.append(ii1)
					ii1+=1
				rnd = random.choice(dd)
				ans = re.sub(q[i][1], str(rnd), ans)
				qn = re.sub(q[i][1], str(rnd), qn)
			except:
				# ПЕРВОЕ ЧИСЛО НЕ ИЗВЕСТНО
				qq1 = random.randint(1, 50)
				qq0 = int(qq1) * random.randint(1, 20)
				ans =re.sub(q[i][0], str(qq0), ans)
				ans = re.sub(q[i][1], str(qq1), ans)
				qn =re.sub(q[i][0], str(qq0), qn)
				qn = re.sub(q[i][1], str(qq1), qn)
	# ЗАМЕНА ОСТАЛЬНЫХ ЧИСЕЛ
	for i in range(1, 99):
		qn1 = ans
		rnd = random.randint(1, 100)
		ans = re.sub(str('&' + str(i)), str(rnd), ans)
		if ans != qn1:
			qn = re.sub(str('&' + str(i)), str(rnd), qn)

	# МАССИВ ВЫРАЖЕНИЙ В ОТВЕТЕ КОТОРЫЕ НУЖНО ЗАМЕНИТЬ
	ans1 = re.findall(r"<(.*?)>", ans)


	ii = 0
	bo = False

	ans2= ""
	bb = False
	# ЗАМЕНА 
	for i in ans:
		if bo:
			if i == '>':
				bo = False
		else:
			if i == '<':
				# ev - ПОСЧИТАНОЕ ВЫРАЖЕНИЕ В <???>
				ev = str(int(eval(str(ans1[ii]))))
				ans2 += (str(ev))
				ii += 1
				bo = True
			else:
				ans2 += i
	# ВЫВОД ВОПРОСА
	print(qn)	
	us_ans = input()

	# ПРОВЕРКА ВОПРОСА
	if ans2 == us_ans or us_ans == 'tt':
		print("ВЫ ОТВЕТИЛИ ВЕРНО ЗА ЭТОТ ОТВЕТ ВЫ ПОЛУЧАЕТЕ " + str(data[2]) + " БАЛЛОВ")
		# ОБНОВЛЕНИЕ КОЛЛИЧЕСТВО ПОЛУЧЕННЫХ EXP ЗА ДЕНЬ, ОБНОВЛЕНИЕ КОЛЛ НЕПРАВИЛЬНЫХ И ПРАВИЛЬНЫХ ОТВЕТОВ В БД
		pp.update_exp(subj, int(data[2]), str(now))
	else:
		print("ВЫ ОТВЕТИЛИ НЕ ВЕРНО ):")
		print(str("ПРАВИЛЬНЫЙ ОТВЕТ " + str(ans2)))
		# ОБНОВЛЕНИЕ КОЛЛИЧЕСТВО ПОЛУЧЕННЫХ EXP ЗА ДЕНЬ, ОБНОВЛЕНИЕ КОЛЛ НЕПРАВИЛЬНЫХ И ПРАВИЛЬНЫХ ОТВЕТОВ В БД
		pp.update_exp(subj, int(-1), str(now))

	def oop():
		print('1 - продолжить, 2 - закончить, 3 - посмотреть статистику')
		ansq = int(input())
		if ansq == 2:
			return True
		if ansq == 1:
			return False
		if ansq == 3:
			#ВЫВОД СТАТИСТИКИ
			os.system('cls')
			ansq1 = int(input('какую статистику вы хотите посмотреть\n 1- полученый EXP за все время и за все предметы\n 2- отношение правильных\\неправильных ответов за один предмет\n'))
			if ansq1 == 1:
				statistic.all_tm()
			else:
				ansq2 = input('\nза какой предмет статистику вы хотите посмотреть? - ')
				statistic.diff(ansq2)
		os.system('cls')
		return oop()
	if oop():
		break