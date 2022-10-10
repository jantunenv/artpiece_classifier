import sqlite3
import pandas
import cv2

def homogenize_images():
	db_fname = "art_metadata.db"

	connection = sqlite3.connect(db_fname)
	c = connection.cursor()

	c.execute(
	'''
	select images.file_path, info.year from info join images on info.id=images.id
	where ((info.material like "%öljy%" and (info.material like "%kangas%" 
	or info.material like "%kankaalle%")) or info.classification = "maalaus") and images.sizex > 600;
	''')

	image_paths = []
	years = []
	for obj in c.fetchall():
		image_paths.append(obj[0])
		years.append(obj[1])

	#take a 500x500 redion from the center of the image

	for path in image_paths:
		im = cv2.imread(path)
		sizex = im.shape[0]
		sizey = im.shape[1]

		xstart = int((sizex - 500) / 2)
		ystart = int((sizey - 500) / 2)

		cropped_im = im[xstart : xstart + 500, ystart : ystart + 500, :]
		cv2.imwrite("cropped_figures/" + path.split('/')[1], cropped_im)

def main():
	homogenize_images()

if __name__ == "__main__":
	main()
