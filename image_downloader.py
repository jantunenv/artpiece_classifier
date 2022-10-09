import json
import urllib.request

def main():
	with open("kansallisgalleria.json", 'r') as f:
		data = json.load(f)

#	print(data[0].keys())

	for object in data:
		id = object["objectId"]
		if(object["multimedia"]):
			link = object["multimedia"][0]["jpg"]["1000"]
			filedata = urllib.request.urlopen(link)
			image_data = filedata.read()
			filename = object["multimedia"][0]["filename"]
#			print(filename)

			with open('figures/'+filename, 'wb') as f:
				f.write(image_data)

main()
