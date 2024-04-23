
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
model = Sequential()

# Step 1 - Convolution
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(150,150,3)))

# Step 2 - Pooling
model.add(MaxPooling2D() )

# Adding a second convolutional layer
model.add(Conv2D(32,(3,3),activation='relu'))

# Step 3 - Pooling
model.add(MaxPooling2D() )

# Adding a third convolutional layer
model.add(Conv2D(32,(3,3),activation='relu'))

# Step 4 - Pooling
model.add(MaxPooling2D() )

# Step 5 - Flattening
model.add(Flatten())

# Step 6 - Full connection
model.add(Dense(100,activation='relu'))

model.add(Dense(1,activation='sigmoid'))

# Compiling the CNN
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset/train',
                                                 target_size = (150, 150),
                                                 batch_size = 16,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/validation',
                                            target_size = (150, 150),
                                            batch_size = 16,
                                            class_mode = 'binary')

model_saved=model.fit_generator(
        training_set,
        epochs=10,
        validation_data=test_set
        )

model.save('mymodel.h5',model_saved)
print("Saved model to disk")