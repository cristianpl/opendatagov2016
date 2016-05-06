from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.db")
conn.text_factory = str  # allows utf-8 data to be stored
cursor = conn.cursor()
cursor.execute("select Latitud, Longitud from tab where Departamento like 'CAPITAL' and Latitud not like 'NULL' and Longitud not like 'NULL' limit 50;")
data = cursor.fetchall()

url = "https://maps.googleapis.com/maps/api/staticmap?center=Corrientes,Argentina&zoom=13&size=800x600&maptype=roadmap&markers=color:red|label:C|"

for row in data:
	#print "LAT: " + row[0] + ", LONG: " + row[1]
	url += row[1] + "," + row[0]
	if row != data[-1]:
		url += "|"
#print url

@app.route('/', methods=['GET', 'POST'])
def mainPage(url=url):
	return render_template("index.html", url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
