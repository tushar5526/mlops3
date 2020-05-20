import pickle
import os

modelStructure = {}

 
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
	modelStructure.update({'flatten' : 'Flatten'})
	
	loop = True

	print('\nSoftmax layer will be added automatically in the last \n')
	
	print('Add a dense layer :: ')


	dlCount = 0
	# Add a dense layer
	while loop:

		dlCount += 1
		neurons  = int(input('Enter Neurons in this layer : '))
		activation = input('Activation Function 1. Relu 2. Sigmoid ')
		
		if activation == '1':
			activation = 'relu'
		elif activation == '2':
			activation = 'sigmoid'
		else:
			activation = 'relu'

		modelStructure.update({'DL' + str(dlCount) : {'Dense' : neurons, 'activation' : activation}})
		tmp = input('Add more layers ? : (y / n) ')

		if tmp == 'y':
			loop = True
		else:
			loop = False


	dlCount += 1

	
	print('Adding dense layer with softmax function by default')
	modelStructure.update({'DL' + str(dlCount) : {'Dense' : 0, 'activation' : 'softmax'}})


	tmp = input('No of epochs : ')
	if not tmp.isnumeric():
		print('\nusing default epoch as 5 \n')
		tmp = 5
	modelStructure.update({'epochs' : tmp})

	tmp = input('\nlearning Rate : ')
	if not tmp.isnumeric():
		print('\nusing default learningRate as 0.001 \n')
		tmp = '0.001'
	modelStructure.update({'learningRate' : tmp})



	modelStructure.update({'DenseLayers' : dlCount})

	for i in modelStructure:
		print(i,' : ',modelStructure[i])
		print('\t|')	
	
	SaveModel()

def FC():

	useDefault = input('\n\tUse default FC HEAD with Flatten -> \n\tDense(512,relu) -> \n\tDense(1024,relu) -> \n\tDense(num_classes,softmax) -> \n\tepochs = 10 -> \n\tLearning Rate = 0.01 \n\n ( y / n ) ')

	if useDefault == 'y':
		modelStructure.update({'flatten' : 'Flatten'})
		modelStructure.update({'DL1' : {'Dense' : 512,'activation' : 'relu'}})
		modelStructure.update({'DL2' : {'Dense' : 1024,'activation' : 'relu'}})
		modelStructure.update({'DL3' : {'Dense' : 0,'activation' : 'softmax'}})
		modelStructure.update({'epochs' : 10})
		modelStructure.update({'learningRate' : '0.001'})
		modelStructure.update({'DenseLayers' : 3})
		SaveModel()
		
		for i in modelStructure:
			print(i,' : ',modelStructure[i])
			print('\t|')

	elif useDefault == 'n':
		MakeFC()


def SetVGG():
	fineTuning = input('Do you want to use fine tuning (y/n) for VGG ')

	modelStructure.update({'model' :'VGG'})
	if fineTuning == 'y':
		modelStructure.update({'fineTuning' : 'y'})
	elif fineTuning == 'n':
		modelStructure.update({'fineTuning' : 'n'})

	else:
		print('using default no for fineTuning ')
		modelStructure.update({'fineTuning' : 'n'})

	FC()

def SetMobileNet():
	fineTuning = input('Do you want to use fine tuning (y/n) for MobileNet ')

	modelStructure.update({'model' : 'MobileNet'})
	if fineTuning == 'y':
		modelStructure.update({'fineTuning' : 'y'})
	elif fineTuning == 'n':
		modelStructure.update({'fineTuning' : 'n'})
	else:		
		print('using default no for fineTuning ')
		modelStructure.update({'fineTuning' : 'n'})

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
	modelStructure.update({'tf' : 'yes'})
	tfLearningFunction()
elif tfLearning == '2':
	modelStructure.update({'tf' : 'no'})
	FromScratch()
else:
	print('Using default Transfer learning')
	tfLearningFunction()
