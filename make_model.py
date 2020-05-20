import pickle

modelStructure = {}
code = []


with open('model.data','rb') as f:
	modelStructure = pickle.load(f)

for i in modelStructure:
	print(i)


lr = (modelStructure['learningRate'])
ep = (modelStructure['epochs'])


importLibs = """
import pickle
import os
from keras.applications import vgg16
from keras.applications import MobileNet
import keras
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
"""

getDataVGG = """

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

"""

#Set variabls num_classes epochs and learning rate

variables = "lr = " + str(lr) + '\nep = ' + str(ep) + '\nol = train_generator.num_classes'

model = ""

if modelStructure['model'] == 'VGG':
	model = """

model = vgg16.VGG16(weights='imagenet',include_top = False,input_shape = (img_rows, img_cols, 3))
model.save('vggtop.h5')"""

else:
	model = """
	
model = MoileNet(weights='imagenet',include_top = False,input_shape = (img_rows, img_cols, 3))
model.save('MobileNet.h5')"""


fineTune = "\n"


if modelStructure['fineTuning'] == 'n':
	fineTune = """

for l in model.layers:
	l.trainable = False

    """


makeModel = """

top_model = model.output
top_model = Flatten()(top_model)

"""

addLayers = ""

for i in range(modelStructure['DenseLayers'] - 1):
	tmp = "\ntop_model = Dense(" + str(modelStructure['DL' + str(i+1)]['Dense']) + ",activation=" + "'" + (modelStructure['DL' + str(i+1)]['activation']) + "'" + ")(top_model)"
	addLayers += tmp


tmp = "\ntop_model = Dense(ol,activation='softmax')(top_model)"

addLayers += tmp


finalModel = """

\nnmodel = Model(inputs = model.input, outputs = top_model)

"""

compileModel = """

\nnmodel.compile(loss = 'categorical_crossentropy'
              ,optimizer = keras.optimizers.Adam(learning_rate = lr), metrics = ['accuracy'])"""



#Enter the number of training and validation samples here

trainModel = """

\nhistory = nmodel.fit_generator(
    train_generator,
    epochs = ep,
    validation_data = validation_generator,
    validation_steps = validation_generator.samples // batch_size)

"""

accuracy="""

try:
	os.system('touch result')
except:
	pass
with open('result','wb') as f:
	pickle.dump(history.history['accuracy'][-1],f)

with open('result','rb') as f:
	print(pickle.load(f))
"""

	


with open('ml_model.py','w') as f:
	f.write(importLibs)
	f.write(getDataVGG)
	f.write(variables)
	f.write(model)
	f.write(fineTune)
	f.write(makeModel)
	f.write(addLayers)
	f.write(finalModel)
	f.write(compileModel)
	f.write(trainModel)
	f.write(accuracy)



f.close()



import os 
os.system('cat ml_model.py')






