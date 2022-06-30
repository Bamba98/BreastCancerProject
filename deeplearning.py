import tensorflow as tf
import cv2
import numpy as np

condition = ['Benign', 'Malignant']

model = tf.keras.models.load_model('./static/models/breastCancer.h5')


def object_detection(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (224, 224))
    image = image.reshape(1, 224, 224, 3)

    predict = model.predict(image)
    index = np.argmax(predict[0])

    return condition[index]

