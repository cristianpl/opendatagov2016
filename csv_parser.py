import csv, sqlite3

#Variables
csvFile = open('Establecimientos2.csv','rbU')
csvReader = csv.reader(csvFile, delimiter = ',')
csvList = []
for row in csvReader:
	csvList.append(row)

colNames = csvList[0]
colTypes = {}
colTypesStr = ''
colNamesStr = ''
colNamesTypesStr = ''
valueTypes = {'int':'"%i"', 'text':'"%s"', 'real':'"%f"'}

#Checking column data types and defining column names
def checkInt(csvList, i):
	try:
		for row in csvList:
			for value in row[i]:
				int(value)
		return True
	except:
		return False

def checkFloat(csvList, i):
	try:
		for row in csvList:
			for value in row[i]:
				float(value)
		return True
	except:
		return False

for i in range(len(colNames)):
	if checkInt(csvList, i):
		colTypes[colNames[i]] = 'int'
	elif checkFloat(csvList, i):
		colTypes[colNames[i]] = 'real'
	else:
		colTypes[colNames[i]] = 'text'

for cn in colNames:
	colNamesStr += cn
	colNamesTypesStr += cn + ' ' + colTypes[cn]
	colTypesStr += valueTypes[colTypes[cn]]
	if cn != colNames[len(colNames) - 1]:
		colNamesStr += ', '
		colNamesTypesStr += ', '
		colTypesStr += ', '

def createDB():
	open('database.db', 'w').close()
	conn = sqlite3.connect('database.db')
	conn.text_factory = str  # allows utf-8 data to be stored
	cursor = conn.cursor()
	cursor.execute('create table tab(%s)' % colNamesTypesStr)
	
	for row in csvList:
		for i in range(len(colTypes)):
			if colTypes[colNames[i]] == 'int':
				row[i] = int(row[i])
			elif colTypes[colNames[i]] == 'real':
				row[i] = float(row[i])
		command = 'insert into tab (%s) values (%s)' % (colNamesStr, colTypesStr)
		command = command % tuple(row)
		cursor.execute(command)
	conn.commit()

def select(query):
	conn = sqlite3.connect('database.db')
	conn.text_factory = str  # allows utf-8 data to be stored
	cursor = conn.cursor()
	cursor.execute(query)
	return cursor.fetchall()

if __name__ == '__main__':
	csvList.remove(colNames)
	createDB()
	print "------- PRINTING THE SELECTED DATA -------"
	data = select('select * from tab;')
	for row in data:
		print row
