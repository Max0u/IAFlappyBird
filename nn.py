from numpy import exp, array, dot, random as nrandom

class NeuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        global learning_rate
        learning_rate = 1
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        # initialize a matrice for weights between INPUTS and HIDDEN layer:
        # 2 * Random - 1 enable to have a number into [-1, 1]
        self.weight_ih = 2 * nrandom.random((hidden_nodes,input_nodes)) - 1
        
        # initialize a matrice for weights between HIDDEN and OUTPUTS layer:
        self.weight_ho = 2 * nrandom.random((output_nodes, hidden_nodes)) - 1

        # initialize a matrice for biais for the HIDDEN layer:
        self.bias_h = 2 * nrandom.random((hidden_nodes, 1)) - 1

        # initialize a matrice for biais for the OUTPUT layer:
        self.bias_o = 2 * nrandom.random((output_nodes, 1)) - 1
        
    def feedforward(self, inputs):
        inputs = inputs.reshape(self.input_nodes, 1)

        # generating the hidden layer
        hidden = dot(self.weight_ih, inputs)
        hidden += self.bias_h
        # activation function
        hidden = self.sigmoid(hidden)

        # generating the output layer
        outputs = dot(self.weight_ho, hidden )
        outputs += self.bias_o
        # activation function
        outputs = self.sigmoid(outputs)

        return hidden, outputs
        
    def train(self, inputs, target_outputs):
        
        hidden, outputs = self.feedforward(inputs)
        inputs = inputs.reshape(self.input_nodes, 1)
        target_outputs = target_outputs.reshape(self.output_nodes, 1)

        # Compute delta HIDDEN - OUTPUT
        output_errors = target_outputs - outputs
        output_delta = self.d_sigmoid(outputs)  * output_errors *  learning_rate

        # Compute delta INPUT - HIDDEN
        hidden_errors = dot(self.weight_ho.T, output_delta)
        hidden_delta = self.d_sigmoid(hidden) * hidden_errors * learning_rate

        # adjust the weight by deltas
        self.weight_ho += dot(output_delta, hidden.T)
        # adjust the bias by its deltas (wich his just the gradient = lr * error * d_sigmoid)
        self.bias_o += output_delta

        # adjust the weight by deltas
        self.weight_ih += dot(hidden_delta, inputs.T)
        # adjust the bias by its deltas (wich his just the gradient = lr * error * d_sigmoid)
        self.bias_h += hidden_delta


    def sigmoid(self, x):
        return 1 / (1 + exp(-x))
    
    def d_sigmoid(self, x):
        # derivative of the sigmoid function
        return x * (1 - x)

class TrainingData(object):
    pass