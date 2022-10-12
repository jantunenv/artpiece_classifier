import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import cv2
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

def main():
	
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
	
	images = []
	for path in image_paths:
		im = cv2.imread("cropped_figures/"+path.split("/")[1])
		images.append(im)

	images = np.asarray(images)

	#Normalize
	min_year = min(years)
	max_year = max(years)
	yeardif = max_year - min_year

	years = np.asarray([float((year - min_year)/yeardif -0.0001) for year in years])

	ind = tf.range(start=0, limit=tf.shape(years)[0], dtype=tf.int32)
	ind_shuffled = tf.random.shuffle(ind)

	images = tf.gather(images, ind_shuffled)
	years = tf.gather(years, ind_shuffled)

	model = Sequential([
	layers.Rescaling(1./255, input_shape=(500, 500, 3)),
	layers.Conv2D(10, 3, padding='same', activation='relu'),
	layers.MaxPooling2D(),
	layers.Conv2D(20, 3, padding='same', activation='relu'),
	layers.MaxPooling2D(),
	layers.Conv2D(40, 3, padding='same', activation='relu'),
	layers.MaxPooling2D(),
	layers.Flatten(),
	layers.Dense(80, activation='relu'),
	layers.Dense(1)
])

	model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=[tf.keras.metrics.MeanSquaredError()])

	epochs = 10
	history = model.fit(images, years, validation_split = 0.2, epochs = epochs)

	loss = history.history['loss']
	val_loss = history.history['val_loss']

	epochs_range = range(epochs)

	plt.figure(figsize=(8, 8))

	plt.subplot(1, 2, 2)
	plt.plot(epochs_range, loss, label='Training Loss')
	plt.plot(epochs_range, val_loss, label='Validation Loss')
	plt.legend(loc='upper right')
	plt.title('Training and Validation Loss')
	plt.show()

if __name__ == "__main__":
	main()
