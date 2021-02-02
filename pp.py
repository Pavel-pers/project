# МОДУЛЬ БАЗЫ ДАНЫХ
import sqlite3

# ФУНКЦИЯ ДОБАВЛЕНИЯ ВОПРОСА 
def add_question(sub,qq,ans,exp):
	# ПОДКЛЮЧЕНИЕ К БД
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	# СОЗДАНИЕ БД ЕСЛИ ЕЕ ЕЩЕ НЕТ
	sql.execute("""CREATE TABLE IF NOT EXISTS questions (
		qq TEXT,
		ans TEXT,
		exp INTEGER,
		subject TEXT
		)""")

	db.commit()

	#ВСТАВКА ВОПРОСА
	sql.execute("INSERT INTO questions VALUES (?, ?, ?, ?)", (str(qq), str(ans), int(exp), str(sub)))
	db.commit()

# ОБНОВЛЕНИЕ КОЛЛ ЕХР И КОЛЛ ПРАВИЛЬНЫХ \ НЕ ПРАВИЛЬНЫХ ОТВЕТОВ
def update_exp(sub, exp1, date):
	# ПОДКЛЮЧЕНИЕ К БД
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	# СОЗДАНИЕ БД ЕСЛИ ЕЕ ЕЩЕ НЕТ
	sql.execute("""CREATE TABLE IF NOT EXISTS user (
	dt TEXT,
	exp INTEGER,
	subject TEXT,
	A INTEGER,
	F INTEGER
	)""")
	db.commit()

	# ВЫБОР СТРОКИ С ТАКИИМИ ЖЕ ДАТАМИ И ПРЕДМЕТАМИ КОТОРЫЕ БЫЛИ ПЕРЕДАНЫ ФУНКЦИИ
	sql = db.cursor()
	sql.execute(f"SELECT * FROM user WHERE dt = '{date}' and subject = '{sub}'")
	data = sql.fetchone()
	# EXP1 == -1 ЗНАЧИТ ЧТО ОТВЕТ БЫЛ НЕ ПРАВИЛЬНЫМ В ЭТОМ СЛУЧАЕ ПРОСТО МЕНЯЕМ КОЛЛ НЕПРАВИЛЬНЫХ ОТВЕТОВ ИНАЧЕ МЕНЯЕМ КОЛЛ ПРАВИЛЬНЫХ ОТВЕТОВ И ЕХР
	# ОТВЕТ ВЕРНЫЙ
	if exp1 != -1:
		# ТАКОЙ СТРОКИ ЕЩЕ НЕТ - ДОБАВЛЯЕМ СРАЗУ С ДАННЫМИ КОТОРЫЕ НУЖНЫ
		if data is None:
			sql.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (str(date), (int(exp1)), str(sub), int(1), int(0)))
			db.commit()
		# ТАКАЯ СТРОКА ЕСТЬ - МЕНЯЕМ ДАННЫЕ
		else:
			expp = int(int(data[1]) + int(exp1))

			sql.execute(f'UPDATE user SET exp = {expp} WHERE dt = "{date}" and subject = "{sub}"')
			a12 = data[3] + 1
			a12 = int(a12)
			sql.execute(f'UPDATE user SET A = {a12} WHERE dt = "{date}" and subject = "{sub}"')
			db.commit()
	# ОТВЕТ НЕ ВЕРНЫЙ
	else:
		# ТАКОЙ СТРОКИ ЕЩЕ НЕТ - ДОБАВЛЯЕМ СРАЗУ С ДАННЫМИ КОТОРЫЕ НУЖНЫ
		if data is None:
			sql.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (str(date), 100, str(sub), int(0), int(1)))
			db.commit()
		# ТАКАЯ СТРОКА ЕСТЬ - МЕНЯЕМ ДАННЫЕ
		else:
			r23 = data[4]+1
			expp = int(int(data[1]) + int(exp1))
			sql.execute(f'UPDATE user SET F = {r23} WHERE dt = "{date}" and subject = "{sub}"')	
			db.commit()

# ПОЛУЧЕНИЕ ВСЕЙ БД user В ВИДЕ МАССИВА ЕСЛИ НЕТ ТАКОЙ БД - СОЗДАЕМ В ИЗБЕЖАНИЕ ОШИБОК
def get_exp():
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	sql.execute("""CREATE TABLE IF NOT EXISTS user (
	dt TEXT,
	exp INTEGER,
	subject TEXT,
	A INTEGER,
	F INTEGER
	)""")
	db.commit()
	lst = []
	for ii in sql.execute("SELECT * FROM user"):
		lst.append(ii)
	return lst

# ПОЛУЧЕНИЕ ВСЕЙ БД questions В ВИДЕ МАССИВА ЕСЛИ НЕТ ТАКОЙ БД - СОЗДАЕМ В ИЗБЕЖАНИЕ ОШИБОК
def get_quetion():
	db = sqlite3.connect('server.db')  
	sql = db.cursor()

	sql.execute("""CREATE TABLE IF NOT EXISTS questions (
		qq TEXT,
		ans TEXT,
		exp INTEGER,
		subject TEXT
		)""")
	db.commit()
	lst = []
	for ii in sql.execute("SELECT * FROM questions"):
		lst.append(ii)
	return lst
