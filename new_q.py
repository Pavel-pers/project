# ПРОГРАММА ДЛЯ РУЧНОГО ДОБАВЛЕНИЕ ВОПРОСА ЧЕРЕЗ КОНСОЛЬ
import pp
def new(sub, qn, ans):
	pp.add_question(sub, qn, ans, int(100))
sub = input()
qn = input()
ans = input()
new	(sub, qn, ans)