
#!/usr/bin/env python
# coding: utf-8

# In[51]:

from keras.applications import vgg16
import keras


# In[52]:


model = vgg16.VGG16(weights='imagenet',include_top = False)
model.save('vggtop.h5')


# In[53]:


for l in model.layers:
    l.trainable = False


# In[54]:


from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D


# In[55]:


top_model = model.output
top_model = GlobalAveragePooling2D()(top_model)
top_model = Dense(1024,activation='relu')(top_model)
top_model = Dense(1024,activation='relu')(top_model)
top_model = Dense(2,activation='softmax')(top_model)


# In[56]:


nmodel = Model(inputs = model.input, outputs = top_model)
print(nmodel.summary())


# In[57]:


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


# In[58]:


from keras.optimizers import RMSprop

nmodel.compile(loss = 'categorical_crossentropy'
              ,optimizer = RMSprop(lr = 0.001), metrics = ['accuracy'])


#Enter the number of training and validation samples here

# We only train 5 EPOCHS 
epochs = 5

history = nmodel.fit_generator(
    train_generator,
    epochs = epochs,
    validation_data = validation_generator,
    validation_steps = validation_generator.samples // batch_size)


# In[59]:


nmodel.save('faceRecog.h5')


# In[63]:


from keras.models import load_model
from PIL import Image
import numpy as np
classifier = load_model('faceRecog.h5')
input_im = Image.open("faceData/1_10.jpg")
input_im.show()
input_original = input_im.copy()

input_im = input_im.resize((224, 224))
display(input_im)
input_im = np.array(input_im)
input_im = input_im / 255.
input_im = input_im.reshape(1,224,224,3)
res = np.argmax(classifier.predict(input_im, 1, verbose = 0), axis=1)
print(res)    
