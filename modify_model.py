import os
import pickle

os.system('sudo docker cp ml:/tf/result .')


maxAccuracy = -1
accuracy = None

var = 0

with open('result','r') as f:
	accuracy = float(f.read())
	print('accuracy after 0 : ',accuracy)


# epochs increase

# adding Dense layers

# learning rate


if accuracy > maxAccuracy:
	maxAccuracy = accuracy
	os.system('sudo docker cp ml:/tf/history .')
	os.system('sudo docker cp ml:/tf/classifier.h5 .')


modelStructure = []


while(accuracy < 0.8 and var < 7):


	if accuracy > maxAccuracy:

		maxAccuracy = accuracy
		os.system('sudo docker cp ml:/tf/history .')
		os.system('sudo docker cp ml:/tf/classifier.h5 .')

	os.system('sudo docker cp ml:/tf/result .')
	
	with open('result','r') as f:
		accuracy = float(f.read())
		print('accuracy after ' + str(var) + ' : ',accuracy)
	
	with open('model.data','rb') as f:
		modelStructure = pickle.load(f)

	var += 1

	if var == 1:
		ep = int(modelStructure['epochs'])
		modelStructure.update({'epochs' : ep})
	
	elif var == 2:
		ep = int(modelStructure['epochs'])
		modelStructure.update({'epochs' : ep})
	
	elif var == 3:
		ep = int(modelStructure['epochs'])
		modelStructure.update({'epochs' : ep})
	
	elif var == 4:
		dlCount = int(modelStructure['DenseLayers'])
		modelStructure.update({'DL' + str(dlCount) : {'Dense' : 256, 'activation' : 'relu'}})
		dlCount = int(modelStructure['DenseLayers']) + 1
		modelStructure.update({'DenseLayers' : dlCount})
	
	elif var == 5:
		dlCount = int(modelStructure['DenseLayers'])
		modelStructure.update({'DL' + str(dlCount) : {'Dense' : 512, 'activation' : 'relu'}})
		dlCount = int(modelStructure['DenseLayers']) + 1
		modelStructure.update({'DenseLayers' : dlCount})
	
	elif var == 6:
		dlCount = int(modelStructure['DenseLayers'])
		modelStructure.update({'DL' + str(dlCount) : {'Dense' : 1024, 'activation' : 'relu'}})
		dlCount = int(modelStructure['DenseLayers']) + 1
		modelStructure.update({'DenseLayers' : dlCount})
	
	elif var == 7:
		lr = float(modelStructure['learningRate'])

		if lr <= 0.001:
			lr = 0.01
		else:
			lr = 0.001
		modelStructure.update({'learningRate' : str(lr)})


	with open('model.data','wb') as f:
		pickle.dump(modelStructure,f)

	os.system("python3 make_model.py")
	os.system('sudo docker exec ml python3 /tf/ml_model.py')

print('max accuracy is ',maxAccuracy)

