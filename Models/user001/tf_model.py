import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras import models, layers

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

#Normalize the images
train_images, test_images = train_images / 255.0, test_images / 255.0

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),  # Flatten the input images
    layers.Dense(128, activation='relu'),  # Fully connected layer with 128 units
    layers.Dense(10, activation='softmax') # Output layer with 10 units for 10 classes
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)