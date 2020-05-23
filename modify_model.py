import os
import pickle


maxAccuracy = -1
accuracy = None

#no of different models tried 
var = 0

#reading the accuracy of the last model from history file
with open('result','r') as f:
	accuracy = float(f.read())
	print('accuracy after 0 : ',accuracy)


# we will try increasing epochs 
# adding more Dense layers

# change learning rate

#save the history of and the best model trained in the folder from docker
if accuracy > maxAccuracy:
	maxAccuracy = accuracy
	os.system('sudo docker cp ml:/tf/history ./Besthistory')
	os.system('sudo docker cp ml:/tf/classifier.h5 ./bestClassifier.h5')


modelStructure = []


#change the model until we get accuracy greater than 80 perecent
#change the model until we had run all different versions of it
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
	#increase epochs
	if var == 1:
		ep = int(modelStructure['epochs']) + 1
		modelStructure.update({'epochs' : ep})
	
	elif var == 2:
		ep = int(modelStructure['epochs']) + 1
		modelStructure.update({'epochs' : ep})
	
	elif var == 3:
		ep = int(modelStructure['epochs']) + 1
		modelStructure.update({'epochs' : ep})
	
	#INCREASE FC LAYERS
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
	
	#CHANGE LEARNING RATE
	elif var == 7:
		lr = float(modelStructure['learningRate'])

		if lr <= 0.001:
			lr = 0.01
		else:
			lr = 0.001
		modelStructure.update({'learningRate' : str(lr)})


	#SAVE THE NEW MODEL.DATA
	with open('model.data','wb') as f:
		pickle.dump(modelStructure,f)

	#RUN THE MAKE_MODEL.PY AGAIN AND THEN RUN THE NEW MODEL IN DOCKER
	os.system("python3 make_model.py")
	os.system('sudo docker exec ml python3 /tf/ml_model.py')

#PRINT THE MAX ACCURACY
print('max accuracy is ',maxAccuracy)

