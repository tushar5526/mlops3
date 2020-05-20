import pickle

modelStructure = []
with open('model.data','rb') as f:
	modelStructure = pickle.load(f)
	


with open('ml_model.py','w') as f:
	f.write(code)
f.close()
import os 
os.system('cat ml_model.py')






