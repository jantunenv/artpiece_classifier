import json
import urllib.request
import sqlite3
import pandas
import cv2

def main():

	connection = sqlite3.connect('art_metadata.db')
	c = connection.cursor()

	c.execute('''
		CREATE TABLE IF NOT EXISTS info
		(id INTEGER PRIMARY KEY, year INTEGER, classification TEXT, material TEXT);
		''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS images
		(id INTEGER PRIMARY KEY, sizex INTEGER, sizey INTEGER, file_path TEXT);
		''')

	with open("kansallisgalleria.json", 'r') as f:
		data = json.load(f)

	for object in data:
		id = object["objectId"]

		if("yearTo" in object.keys()):
			year_end = object["yearTo"]
		else:
			year_end = None

		if("yearFrom" in object.keys()):
			year_start = object["yearFrom"]
		else:
			year_start = None

		if(year_start and year_end):
			year = int(year_start*0.5 + year_end*0.5)
		elif(year_start):
			year = year_start
		elif(year_end):
			year = year_end
		else:
			year = None

		if(object["classifications"]):
			classification = object["classifications"][0]["fi"]
		else:
			classification = None

		materials = ""
		if(object["materials"]):
			for material in object["materials"]:
				materials += material["fi"] + ","
		else:
			materials = None


		if(object["multimedia"] and year):
			filename = object["multimedia"][0]["filename"]
			filepath = 'figures/'+filename

			im = cv2.imread(filepath)
			sizex = im.shape[0]
			sizey = im.shape[1]

			c.execute("INSERT INTO info VALUES(%s, %s, '%s', '%s');"%(str(id), str(year), str(classification), str(materials)))
			c.execute("INSERT INTO images VALUES(%s, %s, %s, '%s');"%(str(id), str(sizex), str(sizey), str(filepath)))


	c.execute(
	'''
	SELECT info.id, info.year, info.classification, info.material, images.sizex, images.sizey, images.file_path 
	FROM images INNER JOIN info ON images.id=info.id;
	''')

	df = pandas.DataFrame(c.fetchall())
	print(df)
	connection.commit()

main()
