
import pickle
import os
from keras.applications import vgg16
from keras.applications import MobileNet
import keras
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D


img_rows, img_cols = 224,224
from keras.preprocessing.image import ImageDataGenerator

train_data_dir = 'faceData/train/'
validation_data_dir = 'faceData/test/'

# Let's use some data augmentaiton 
train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=45,
      width_shift_range=0.3,
      height_shift_range=0.3,
      horizontal_flip=True,
      fill_mode='nearest')
 
validation_datagen = ImageDataGenerator(rescale=1./255)
 
# set our batch size (typically on most mid tier systems we'll use 16-32)
batch_size = 32
 
train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_rows, img_cols),
        class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_rows, img_cols),
        class_mode='categorical')

lr = 0.001
ep = 1
ol = train_generator.num_classes

model = vgg16.VGG16(weights='imagenet',include_top = False,input_shape = (img_rows, img_cols, 3))
model.save('vggtop.h5')

for l in model.layers:
	l.trainable = False

    

top_model = model.output
top_model = Flatten()(top_model)


top_model = Dense(256,activation='relu')(top_model)
top_model = Dense(512,activation='relu')(top_model)
top_model = Dense(1024,activation='relu')(top_model)
top_model = Dense(ol,activation='softmax')(top_model)


nmodel = Model(inputs = model.input, outputs = top_model)




nmodel.compile(loss = 'categorical_crossentropy'
              ,optimizer = keras.optimizers.Adam(learning_rate = lr), metrics = ['accuracy'])


history = nmodel.fit_generator(
    train_generator,
    epochs = ep,
    validation_data = validation_generator,
    validation_steps = validation_generator.samples // batch_size)



try:
	os.system('touch result')
except:
	pass
with open('result','wb') as f:
	pickle.dump(history.history['accuracy'][-1],f)

with open('result','rb') as f:
	print(pickle.load(f))
