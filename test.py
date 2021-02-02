#ПРОГРАММА ДОБАВЛЯЮЩЯЯ ВОПРОСЫ ИЗ f И f1 В БД  

import pp

def new(sub, qn, ans):
	pp.add_question(sub, qn, ans, int(100))

f = open('f.txt', encoding = 'UTF-8')

a = []
for i in f:
	a.append(i.replace('\n', ''))

ii = 0
print('math')
while ii < len(a):
	new('math', a[ii], a[ii+1])
	print(ii)
	ii+=2

f1 = open('f1.txt', encoding = 'UTF-8')
a1 = []
for i in f1:
	a.append(i.replace('\n', ''))

print('eng')
while ii < len(a1):
	new('eng', a[ii], a[ii+1])
	print(ii)
	ii+=2
