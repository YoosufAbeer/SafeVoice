# nurone for ai

# import the libraries
import random
import math
# the data used for training the model
Data = [[1,8,4,0],[2,7,3,0],[5,8,2,1],[7,6,3,1],[10,8,1,1],[3, 8, 3, 0],[6, 7, 2, 1],[8, 6, 2, 1],[1, 8, 4, 0],
        [2, 7, 3, 0],[3, 9, 4, 0],[4, 7, 4, 0],[5, 8, 2, 1],[6, 7, 2, 1],[7, 6, 3, 1],[8, 7, 2, 1],[9, 8, 1, 1],
        [10, 8, 1, 1]]
TrainingData = Data[:10]
TestData = Data[10:]

# set the weights, bias, learning rate, and the smallchange value 
weight1 = 0
weight2 = 0
weight3 = 0
bias = 0
learning_rate = 0.01
small_change = 0.001

# update the weights as new ones
weight1_plus = 0
weight2_plus = 0
weight3_plus = 0

# neuron class
class NeruralNetwork:
    def __init__(self):
        self.weight1 = random.uniform(-1, 1)
        self.weight2 = random.uniform(-1, 1)
        self.weight3 = random.uniform(-1, 1)
        self.bias = random.uniform(-1, 1)
# store all the fuctions
    def predict(self, input_Val1, input_Val2, input_Val3):
        # calculate the output
        rawoutput = (input_Val1 * self.weight1) + (input_Val2 * self.weight2) + (input_Val3 * self.weight3) + self.bias
        return sigmoid(rawoutput)
    def train(self, input_Val1, input_Val2, input_Val3, expected_output):
        # cross check the output
        pridiction = network.predict(input_Val1, input_Val2, input_Val3)
        loss = cal_loss(expected_output, pridiction)
        
        # calculate the gradients
        loss_gradient = 2 * (pridiction - expected_output)
        
        sigmoid_gradient = pridiction * (1 - pridiction)
        
        gradient_rawoutput = loss_gradient * sigmoid_gradient
        
        gradient1 = gradient_rawoutput * input_Val1
        gradient2 = gradient_rawoutput * input_Val2
        gradient3 = gradient_rawoutput * input_Val3
        
        gradient_bias = gradient_rawoutput
    
        # update the weights and bias
        self.weight1 -= learning_rate * gradient1
        self.weight2 -= learning_rate * gradient2
        self.weight3 -= learning_rate * gradient3
        self.bias -= learning_rate * gradient_bias

network = NeruralNetwork()

def cal_loss(expected_output, pridiction):
    loss = (expected_output - pridiction) ** 2
    return loss

def sigmoid(rawoutput):
    return 1 / (1 + math.exp(-rawoutput))

# epochs
for epochs in range(1000):
    #randomize the training data
    training_copy = TrainingData.copy()
    random.shuffle(training_copy)
    # the verification of the output
    for input_Val1, input_Val2, input_Val3, expected_output in training_copy:
        # trainig 
        network.train(input_Val1, input_Val2, input_Val3, expected_output)

# output the results
print("final weight1:", network.weight1)
print("final weight2:", network.weight2)
print("final weight3:", network.weight3)
print("final Bias:", network.bias)

# for counting
correct = 0
# final testing of the model
print("\n---TESTING---")
for input_Val1, input_Val2, input_Val3, expected_output in TestData:
    pridiction = network.predict(input_Val1, input_Val2, input_Val3)

    # round the pridiction to 0 or 1
    if pridiction >= 0.5:
        pridiction = 1
    else:
        pridiction = 0

    # count the correct pridictions
    if pridiction == expected_output:
        correct += 1

    # output the results
    print("pridiction:", pridiction,)
    print("expected output:", expected_output)

# calculate the accuracy
accuracy = correct / len(TestData)

# output the accuracy
print("\nAccuracy:", accuracy * 100, "%")