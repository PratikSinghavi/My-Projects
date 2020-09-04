import numpy as np
#from scipy.special import softmax
import copy
import sys

def load_dataset(train='train_image.csv',train_l='train_label.csv',test='test_image.csv'):
	train_images = np.genfromtxt(train,delimiter=',') / 255#.reshape(60000,784)
	train_labels = np.genfromtxt(train_l,delimiter='')
	test_images = np.genfromtxt(test,delimiter=',') / 255#.reshape(10000,784)
	#test_labels = np.genfromtxt('test_label.csv',delimiter='')

	return ((train_images,train_labels,test_images))#,(test_images,test_labels))#

def init():
	global b2,w2,b1,w1
	#np.random.seed(0)	

	w1 = np.random.randn(784,300) / np.sqrt(784)
	b1 = np.random.randn(1,300) / np.sqrt(300)

	w2 = np.random.randn(300,10) / np.sqrt(300)
	b2 = np.random.randn(1,10) / np.sqrt(300)

def activate(Z):
	return np.array([i if i>0 else 0 for i in np.squeeze(Z)])

def relu_derivative(Z):
	return np.array([1 if i>0 else 0 for i in np.squeeze(Z)])

def Softmax(z):
	f = np.exp(z - np.max(z))  # shift values
	sum_f = np.sum(f)
	return f / sum_f
	#return np.exp(z)/sum(np.exp(z)) #1/sum(np.exp(z)) * np.exp(z)

def cross_entropy_loss(z,label_ind):
		# implement the cross entropy error
	return -np.log(z[label_ind])


def forward_pass(img,label):
	global b2,w2,b1,w1
	x0 = img.reshape(1,784)

	z1 = np.matmul(x0,w1).reshape(1,300) + b1
	x1 = activate(z1).reshape(1,300)
	#print(x1)
	
	z2 = np.matmul(x1,w2).reshape(1,10) + b2
	softmax_x = Softmax(z2).squeeze()
	#print(softmax_x)

	error = cross_entropy_loss(softmax_x,label)
	#print(error)

	return [z1,x1,z2,softmax_x,error]
									#Z H U
def calculate_derivatives(img,label,z1,x1,z2,softmax_op,error): #backprop
	global b2,w2,b1,w1
	X = np.zeros([1,10])
	X[0][label] = 1
	#print(X)
	#print(softmax_op)
	dZ2 = (-(X - softmax_op)).reshape((1,10))
	db2 = copy.copy(dZ2)
	#print(db2)
	dW2 = np.matmul(x1.transpose(),dZ2) #2ndlayer bias
	#print(dW2.shape)
	mmd = np.matmul(dZ2,w2.transpose())
	db1 = mmd.reshape(1,300) * relu_derivative(z1).reshape(1,300) #element wise multiplication
	#print(db1.shape)
	dW = np.matmul(img.reshape((784,1)),db1.reshape((1,300)))
	#print(dW.shape)

	return [dW2,db2,db1,dW]

def evaluate_testdata(X_test):
	print('Test_start')
	prediction_arr = np.array([])
	for i in range(len(X_test)):
		x = X_test[i][:]
		prediction = np.argmax(forward_pass(x,0)[3])
		prediction_arr = np.append(prediction_arr,prediction)
	#print(prediction_arr.shape)
	#print(prediction_arr)
	return prediction_arr

def modify_weights(learning_rate,gradients):
	global b2,w2,b1,w1
	w2 -= learning_rate*gradients[0]
	b2 -= learning_rate*gradients[1]
	b1 -= learning_rate*gradients[2]
	w1 -= learning_rate*gradients[3]

def backprop_learn():
	print('Learning...')
	
	rand_indices = np.random.choice(len(x_train), 60000, replace=True)
	count = 1
	#print(len(rand_indices))

	for i in rand_indices:
		Z1,X1,Z2,Softmax_op,error=forward_pass(x_train[i],y_train[i])
		#print(np.argmax(Softmax_op),error)
		gradients = calculate_derivatives(x_train[i],y_train[i],Z1,X1,Z2,Softmax_op,error)
		modify_weights(0.01,gradients)

		count= count+1

def write_result(fname):
	with open(fname,'w') as f:
		for i in prediction_arr:
			f.write(str(int(i))+'\n')
	print('File written')



#================================================================= MAIN =================================================================#
global b2,w2,b1,w1

############################ Commandline Args ############################

if len(sys.argv) > 1:
	print('Command line arguments received')
	(x_train,y_train,x_test) = load_dataset(sys.argv[1],sys.argv[2],sys.argv[3])

else:
	print('No arguments received; Using default')
	(x_train,y_train,x_test) = load_dataset()


############################# Preprocessing ##############################
print('Loading Complete')
x_train = np.float32(x_train)
y_train = np.int32(np.array(y_train))
x_test = np.float32(x_test)
y_test = np.int32(np.zeros(x_test.shape[0]))#np.int32(np.array(y_test))


############################# Train & Test ###############################
init()
backprop_learn()
prediction_arr = evaluate_testdata(x_test)
write_result('test_predictions.csv')

#========================================================================================================================================#



