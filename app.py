#from signal import valid_signals
#from typing import Dict
from flask import *
import mysql.connector
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key="week4test3"
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="website"
    )
#API-1
@app.route("/api/attractions")
def attractions():
	try:
		keyPage=request.args.get("page","0")
		keyWord=request.args.get("keyword",None)
		x=int(keyPage)*12
		print(keyPage)
		data=[]
		info=("id","nextPage","name","category","description","address","transport","mrt","latitude","longitude","images")
		if keyWord==None:
			for i in range(x+1,x+13):
				sql="SELECT id,nextPage,name,category,description,address,transport,mrt,latitude,longitude,images FROM website.taipei_attrations_website WHERE id=%s"
				val=(str(i),)
				#print(val)
				mycursor=mydb.cursor()
				mycursor.execute(sql,val)
				mydata=mycursor.fetchone()
				#print(mydata)
				dic=[{info[j]:mydata[j] for j in range(len(mydata)-1)}]
				data=data+dic
			resP={"nextpage":keyPage,"data":data}
			print(data)
			#mydb.close()
			return str(resP)
		else: 
			sql="SELECT id,nextPage,name,category,description,address,transport,mrt,latitude,longitude,images FROM website.taipei_attrations_website WHERE nextPage=%s and name LIKE %s"
			keyWord='%'+keyWord.strip('"')+'%'
			val=(keyPage,keyWord)
			print(val)
			mycursor=mydb.cursor()
			mycursor.execute(sql,val)
			mydata=mycursor.fetchone()
			print(mydata)
			data=[{info[j]:mydata[j] for j in range(len(mydata)-1)}]
			resP={"nextpage":keyPage,"data":data}
			print(data)
			#mydb.close()
			return str(resP)
		#mydb.close()
		#return render_template("index.html")
		#mycursor.close()
	except: 
		error={"error":True,"message":"連結錯誤或無搜尋配對"}
		return str(error)
#API-2
@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
	try:
		keyId=attractionId
		info=("id","name","category","description","address","transport","mrt","latitude","longitude","images")
		sql="SELECT id,name,category,description,address,transport,mrt,latitude,longitude,images FROM website.attraction WHERE id=%s"
		val=(str(keyId),)
		print(val)
		mycursor=mydb.cursor()
		mycursor.execute(sql,val)
		mydata=mycursor.fetchone()
		print(mydata)
		data={info[j]:mydata[j] for j in range(len(mydata))}
		resP={"data":data}
		print(data)
		#mydb.close()
		return str(resP)
		#mydb.close()
		#return render_template("index.html")
		#mycursor.close()
	except: 
		error={"error":True,"message":"自訂的錯誤訊息"}
		return str(error)
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000)
#id,nextPage,name,category,description,address,transport,mrt,latitude,longitude,images
