#=============================
#includes from Microsoft docs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import tensorflow as tf
import tensorflow_io as tfio
import IPython.display as ipd
#=============================
#includes from geeksforgeeks

from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model

#============================

if __name__ == "__main__":
    train_directory = r'data\train'
    test_directory = r'data\test'

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        train_directory, labels='inferred', label_mode='int', image_size=(256, 256), seed=123, 
        validation_split=0.2, subset='validation')

    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_directory, labels='inferred', label_mode='int', image_size=(256, 256), 
        validation_split=None, subset=None)

    class_names = train_ds.class_names
    print(class_names)

    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
            
    plt.show()

    num_classes = 2
    img_height = 256
    img_width = 256

    model = tf.keras.Sequential([
      tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
      tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
      tf.keras.layers.MaxPooling2D(),
      tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
      tf.keras.layers.MaxPooling2D(),
      tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
      tf.keras.layers.MaxPooling2D(),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(num_classes)
    ])

    learning_rate = 0.125

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    optimizer = tf.keras.optimizers.SGD(learning_rate)
    metrics = ['accuracy']
    model.compile(optimizer, loss_fn, metrics)

    # Set the epocks
    epochs = 20
    print('\nFitting:')

    # Train the model.
    history = model.fit(train_ds, epochs=epochs)

    model.summary()

    correct = 0
    batch_size = 0
    for batch_num, (X, Y) in enumerate(test_ds):
        batch_size = len(Y)
        pred = model.predict(X)
        for i in range(batch_size):
            predicted = np.argmax(pred[i], axis=-1)
            actual = Y[i]
            #print(f'predicted {predicted}, actual {actual}')
            if predicted == actual:
                correct += 1
        break

    print(f'Number correct: {correct} out of {batch_size}')
    print(f'Accuracy {correct / batch_size}')

    #==================================
    #Save the model.

    # saving and loading the .h5 model
     
    # save model
    model.save('gfgModel.h5')
    print('Model Saved!')
     
    # load model
    savedModel=load_model('gfgModel.h5')
    savedModel.summary()