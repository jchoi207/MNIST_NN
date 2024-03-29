import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
data = pd.read_csv('Desktop/NN/digit-recognizer/train.csv')

data = np.array(data)

m, n = data.shape #initialize the dimensions of set
print(m, n)
np.random.shuffle(data) #shuffle the data 


data_dev = data[0:1000].T # 785 x 1000 
print(data_dev.shape) 
Y_dev = data_dev[0] # 0th element of each vector represents the correct number
X_dev = data_dev[1:n] # the actual pixels grayscale values
X_dev = X_dev / 255.

data_train = data[1000:m].T # 785 x m - 1000
Y_train = data_train[0]
X_train = data_train[1:n] 
X_train = X_train / 255.

def initialization(): 
    b1 = np.random.rand(10, 1) - 0.5 
    b2 = np.random.rand(10, 1) - 0.5
    W1 = np.random.rand(10, 784) - 0.5
    W2 = np.random.rand(10, 10) - 0.5
    return W1, b1, W2, b2

def ReLU(Z):
    return np.maximum(0, Z) # element wise, goes through each element in Z, if > 0, then max != 0 

def softmax(Z):
    return np.exp(Z) / sum(np.exp(Z))

def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2 
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2

def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y

def deriv_ReLU(Z):
    return Z > 0 # boolean converted to numbers, 
    
def back_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2


def update(W1, b1, W2, b2,dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1 
    b1 = b1 - alpha * db1 
    W2 = W2 - alpha * dW2 
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2 
    

def get_predictions(A2):
    return np.argmax(A2, 0)

def accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size

def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = initialization()
    l = []
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)
            accuracy = accuracy(predictions, Y)
            l.append(accuracy)
            print(accuracy(predictions, Y))
            
    return W1, b1, W2, b2, l


runs = 500
W1, b1, W2, b2, l = gradient_descent(X_train, Y_train, 0.10, runs)

x = np.linspace(0, runs - 10 ,50)


plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.axhline(y=0.86)
plt.title("Asymptotic Bound in Accuracy of a 2 layer NN using the MNIST data set")
plt.plot(x, l)
