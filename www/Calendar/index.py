import time

def run(req):

	monthNameAbrv = ['', 'Jan', 'Fev', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dez']

	months = []
	for i in xrange(1, 13):
		months.append({
			'name' : monthNameAbrv[i],
			'day' : genMonth(i)
		})

	output = {
		'weekday' : genWeekday(),
		'month' : months
	}

	# f = open("index2.html", "w")
	# f.write(template.genTemplate(output))
	# f.close()

	# return "template Generated"
	return template.process('index.html', output)

def genMonth(x):
	maxDayPerMonth = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if (x == 2) and ((2012 % 4) == 0): maxDayPerMonth[2] = 29

	# Mes anterior a X
	prevMonth = x-1
	if prevMonth < 1: prevMonth = 12

	# Info do Mes X
	sec = time.mktime((2012, x, 1, 0, 0, 0, 0, 0, 0))
	info = time.localtime(sec)

	month = []
	day = 0
	wday = info.tm_wday-1
	i = 0
	while i < 37:
		ghost = 'ghost'

		number = maxDayPerMonth[prevMonth] - wday + day

		if number > maxDayPerMonth[prevMonth]:
			number -= maxDayPerMonth[prevMonth]
			ghost = ''

		if number > maxDayPerMonth[x] and ghost == '':
			number -= maxDayPerMonth[x]
			ghost = 'ghost'

		weekend = ''
		if (i % 7) == 5 or (i % 7) == 6:
			weekend = 'weekend'

		month.append({
			'number' : number,
			'ghost' : ghost,
			'weekend' : weekend
		})
		if wday > 0: wday -= 1
		else:
			day += 1

		i += 1

	return month

def genWeekday():
	arr = ['Mon', 'Thu', 'Wen', 'Thr', 'Fri', 'Sat', 'Sun']
	outArr = []
	for i in xrange(37):
		outArr.append({
			'name' : arr[i%7]
		})

	return outArr