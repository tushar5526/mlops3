import pickle
import os

modelStructure = []

 
def SaveModel():
	with open('model.data','wb') as f:
		pickle.dump(modelStructure,f)

def MakeFC():

	loop = True

	"""
	tmp = input('Do you want to add a Conv2D or MaxPool layer (y/n) ')

	if tmp == 'y':
		loop = True
	else:
		loop = False


	# add conv2d or max layer
	while loop:
		x = input("\n Add a layer \n\t 1. Conv2D \n\t 2. MaxPool \n\t")

		if x == '1':
			filters = input('filters')
			activation = input('Activation 1. Relu 2. Sigmoid 3. tanh 4. Softmax ')
		
		elif x == '2':
			pass

		else: 
			pass

		print('Add more layers ? : (y / n) ')
	"""

	print('\nAdding a flatting layer for dense layers ')
	modelStructure.append('Flatten')
	
	loop = True

	print('\nSoftmax layer will be added automatically in the last \n')
	
	print('Add a dense layer :: ')


	# Add a dense layer
	while loop:

		neurons  = input('Enter Neurons in this layer : ')
		activation = input('Activation Function 1. Relu 2. Sigmoid ')
		
		if activation == '1':
			activation = 'relu'
		elif activation == '2':
			activation = 'sigmoid'
		else:
			activation = 'relu'

		modelStructure.append({'Dense' : neurons, 'activation' : activation})
		tmp = input('Add more layers ? : (y / n) ')

		if tmp == 'y':
			loop = True
		else:
			loop = False

	
	print('Adding dense layer with softmax function by default')
	modelStructure.append({'Dense' : 'end', 'activation' : 'softmax'})


	tmp = input('No of epochs : ')
	if not tmp.isnumeric():
		print('\nusing default epoch as 10 \n')
		tmp = 10
	modelStructure.append({'epochs' : tmp})

	tmp = input('\nlearning Rate : ')
	if not tmp.isnumeric():
		print('\nusing default learningRate as 0.001 \n')
		tmp = 0.001
	modelStructure.append({'learningRate' : tmp})


	for i in modelStructure:
		print(i)
		print('\t|')

	SaveModel()

def FC():

	useDefault = input('\n\tUse default FC HEAD with Flatten -> \n\tDense(512,relu) -> \n\tDense(1024,relu) -> \n\tDense(num_classes,softmax) -> \n\tepochs = 10 -> \n\tLearning Rate = 0.01 \n\n ( y / n ) ')

	if useDefault == 'y':
		modelStructure.append('Flatten')
		modelStructure.append({'Dense : 512','activation : relu'})
		modelStructure.append({'Dense : 1024','activation : relu'})
		modelStructure.append({'Dense : end','activation : softmax'})
		modelStructure.append({'epochs' : '10'})
		modelStructure.append({'learningRate' : '0.001'})
		SaveModel()
		
		for i in modelStructure:
			print(i)
			print('\t|')

	elif useDefault == 'n':
		MakeFC()


def SetVGG():
	fineTuning = input('Do you want to use fine tuning (y/n) for VGG ')

	modelStructure.append('VGG')
	if fineTuning == 'y':
		modelStructure.append('y')
	elif fineTuning == 'n':
		modelStructure.append('n')

	else:
		print('using default no for fineTuning ')
		modelStructure.append('n')

	FC()

def SetMobileNet():
	fineTuning = input('Do you want to use fine tuning (y/n) for MobileNet ')

	modelStructure.append('MobileNet')
	if fineTuning == 'y':
		modelStructure.append('y')
	elif fineTuning == 'n':
		modelStructure.append('n')
	else:		
		print('using default no for fineTuning ')
		modelStructure.append('n')

	FC()



def tfLearningFunction():
	modelTF = input('Do you want to use VGG (1) or MobileNet (2) ')

	if modelTF == '1':
		SetVGG()
	elif modelTF == '2':
		SetMobileNet()
	else:
		print('Using default MobileNet for Transfer Learning ')
		SetMobileNet()


def FromScratch():
	print("Not supported yet, use transfer learning only")





print('Welcome Message ')

tfLearning = input('Do you want Transfer Learning (1) or Make model from scratch (2) ')

if tfLearning == '1':
	tfLearningFunction()
elif tfLearning == '2':
	FromScratch()
else:
	print('Using default Transfer learning')
	tfLearningFunction()

