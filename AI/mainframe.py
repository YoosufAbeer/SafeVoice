# import the libraries
import random
import math
# the data used for training the model
Data = []
# simulate data
seen = set()
# loop to create data
while len(Data) < 100:
    sleep = random.randint(4, 10)
    studied = random.randint(0, 8)
    procastinated = random.randint(0, 8)
    # initalize the data 
    inputs = (sleep, studied, procastinated)
    # check for duplicates
    if inputs in seen:
        continue
    seen.add(inputs)
    # calculate the score
    score = studied +0.5  * sleep - procastinated
    # finds out the expected output
    if score >= 5:
        expected_output = 1
    else:
        expected_output = 0
    # add expected output to the data array
    Data.append([sleep, studied, procastinated, expected_output])
# check for dulicate data
UniqueData = []

for example in Data:
    if example not in UniqueData:
        UniqueData.append(example)
# output the len to verify the data 
print("original data: ", len(Data))
print("unique data:",len(UniqueData))
# shuffle the unique data
random.shuffle(UniqueData)
# split the data into training and testing 
split_index = int(len(UniqueData) * 0.8)
# set the training and test data
TrainingData = UniqueData[:split_index]
TestData = UniqueData[split_index:]
# output the length of the training and test data
print("Training Data:", len(TrainingData))
print("Test Data:", len(TestData))

# set the weights, bias, learning rate, and the smallchange value 
weight1 = 0
weight2 = 0
weight3 = 0
bias = 0
learning_rate = 0.2
small_change = 0.001

# update the weights as new ones
weight1_plus = 0
weight2_plus = 0
weight3_plus = 0

# basic fuctions that are needed
def cal_loss(expected_output, pridiction):
    loss = (expected_output - pridiction) ** 2
    return loss

def sigmoid(rawoutput):
    return 1 / (1 + math.exp(-rawoutput))

# neuron class
class NeruralNetwork:
    def __init__(self):
        # initialize the hidden nurones 
        self.hidden_size = 7
        # initialize the weights and bias
        self.weights = [
            [random.uniform(-1, 1)for _ in range(3)]
            for _ in range(self.hidden_size)
        ]
        self.bias = [
            random.uniform(-1, 1)
            for _ in range(self.hidden_size)
            ]

        # initialize the "OUTPUT"weights and bias
        self.output_weights = [
                random.uniform(-1, 1)
                for _ in range(self.hidden_size)
            ]
        self.output_bias = random.uniform(-1, 1)
# store all the fuctions
    def predict(self, input_Val1, input_Val2, input_Val3):
        # make arrary
        hidden_outputs = self.predict_all(input_Val1, input_Val2, input_Val3)
        # initialization
        rawoutput = 0
        # make the pridiction
        for output, weight in zip(hidden_outputs, self.output_weights):
            rawoutput += output * weight
        rawoutput += self.output_bias
        # sigmoid the pridiction
        pridiction = sigmoid(rawoutput)
        return pridiction
    def predict_all(self, input_Val1, input_Val2, input_Val3):
        # make arrrays
        inputs = [input_Val1, input_Val2, input_Val3]
        outputs = []
        # preform calculations
        for nurone in range(self.hidden_size):
            rawoutput = 0
            for input_value, weght in zip(inputs, self.weights[nurone]):
                rawoutput += input_value * weght
            rawoutput += self.bias[nurone]
            output = sigmoid(rawoutput)
            outputs.append(output)
        return outputs
    def train(self, input_Val1, input_Val2, input_Val3, expected_output, learning_rate):
        # create arrays needed
        inputs = [input_Val1, input_Val2, input_Val3]
        # get the pridictions
        hidden_outputs = self.predict_all(input_Val1, input_Val2, input_Val3)
        pridiction = self.predict(input_Val1, input_Val2, input_Val3)
        # calculate the gradient for the output layer
        loss_gradient = 2 * (pridiction - expected_output)
        sigmoid_gradient = pridiction * (1 - pridiction)
        output_gradient = loss_gradient * sigmoid_gradient
        # show the old output weights
        old_output_weights = self.output_weights.copy()
        # update the weights and bias
        for i in range(self.hidden_size):
            gradient = output_gradient * hidden_outputs[i]
            self.output_weights[i] -= learning_rate * gradient
        self.output_bias -= learning_rate * output_gradient
        # calculate the gradient for the hidden layer
        for nurones in range(self.hidden_size):
            hidden_output = hidden_outputs[nurones]
            hidden_gradient = (output_gradient * old_output_weights[nurones] * hidden_output * (1 - hidden_output))
            for i in range(3):
                gradient = hidden_gradient * inputs[i]
                self.weights[nurones][i] -= learning_rate * gradient
            self.bias[nurones] -= learning_rate * hidden_gradient
# arrays for checking the reliability 
run_accuracies = []
run_losses = []
mistake_count = {}
# number or runs done
number_of_runs = 10000
# repeats the experiment 50 times
for run in range(number_of_runs):
    # creat a fresh network every time
    network = NeruralNetwork()
    # train the network 
    for epochs in range(1000):
        # setting up the requierd data
        trainnig_copy = TrainingData.copy()
        random.shuffle(trainnig_copy)
        # initalize loss
        total_loss = 0
        # run the network
        for input_Val1, input_Val2, input_Val3, expected_output in trainnig_copy:
            # calculate loss before update
            pridiction = network.predict(input_Val1, input_Val2, input_Val3)
            total_loss += cal_loss(expected_output,pridiction)
            # train the network 
            network.train(input_Val1, input_Val2, input_Val3, expected_output, learning_rate)
        # calculate the avrage loss for the epoch
        average_loss = total_loss / len(trainnig_copy)
    # save the final loss data for the run
    run_losses.append(average_loss)
    # another initalization
    correct = 0
    test_total_loss = 0
    # test the trained network
    for input_Val1, input_Val2, input_Val3, expected_output in TestData:
        # get the raw network value
        raw_pridiction = network.predict(input_Val1, input_Val2, input_Val3)
        # calculate the loss for the test data
        test_total_loss += cal_loss(expected_output, raw_pridiction)
        # convert the raw pridiction to a 1 or 0
        if raw_pridiction >= 0.5:
            pridiction_class = 1
        else:
            pridiction_class = 0
        # check if the pridiction is correct 
        if pridiction_class == expected_output:
            correct += 1
        else:
            # store the examples as a tuple
            example = (input_Val1, input_Val2, input_Val3, expected_output)
            # add one to its mistake count 
            if example not in mistake_count:
                mistake_count[example] = 0
            mistake_count[example] += 1
    # calculate the average loss for the test data
    average_test_loss = test_total_loss / len(TestData)
    # calculate and save the accuracy
    accuracy = correct / len(TestData)
    run_accuracies.append(accuracy)
    print(
        "Run:", run + 1,
        "|Accuracy:", accuracy * 100, "%",
        "|Final loss:", average_loss,
        "|Test loss:", average_test_loss
    )
# detrmine which runs where 100% successful
successful_runs = 0
for accuracy in run_accuracies:
    if accuracy == 1.0:
        successful_runs += 1
#summurize all 50 tests
average_accuracy = sum(run_accuracies) / len(run_accuracies)
best_accuracy = max(run_accuracies)
worst_accuracy = min(run_accuracies)
average_final_loss = sum(run_losses) / len(run_losses)
# output the details
print("\n---RESULTS---")
print("Total runs: ", number_of_runs)
print("Perfect runs: ", successful_runs, "/", number_of_runs)
print("Average accuracy: ", average_accuracy * 100, "%")
print("Best accuracy: ", best_accuracy* 100, "%")
print("worst accuracy: ", worst_accuracy* 100, "%")
print("Average final training loss: ",average_final_loss)
# show all the most common mistakes
print("\n---MOST COMMON MISTAKES---")
print("Unique mistake entries:", len(mistake_count))

for example, count in mistake_count.items():
    print(repr(example), "->", count)
# manual testing of the model
print("\n---MANUAL TESTING---")
# testExamples
testExamples = [[1,8,4,0],[10,8,1,1],[4, 8, 3, -1]]
# loop through the test examples
for input_Val1, input_Val2, input_Val3, expected_output in testExamples:
    # make the pridiction
    pridiction = network.predict(input_Val1, input_Val2, input_Val3)
    # print the pridiction & expected output
    print("pridiction: ", pridiction)
    print("expected output: ", expected_output)
print("\n--- TESTING COMMON MISTAKES ---")

print("Example 1:", network.predict(4, 8, 5))
print("Expected: 1")

print("Example 2:", network.predict(7, 8, 6))
print("Expected: 1")