import torch
#nn contains Neural network layers, conv net layer,recurrent layer and activation functions etc
import torch.nn as nn
# algorithms used for adjusting weights and biases on the nodes, includes stochastic, gradient decent, Adam RMSprop
import torch.optim as optim
# contains activation functions like ReLu, sigmoid and tanh and los functions like cross entropy
import torch.nn.functional as F
# pythoin function to allow interactiveing with the operating system files and folders
import os

#create two classes, one for model and one for trainer
class Linear_QNet(nn.module):
    def __init__ (self, input_size, hidden_size, output_size):
        super().__init__()
    # building the NN layers  layer 1 get the input_size as input and hidden_size as output
    #layer 2 get hidden as input and output as output
        self.linear1=nn.Linear(input_size, hidden_size)
        self.linear2=nn.linear(hidden_size, output_size)
     #then we have to implement the forward function. x is the tensor
    def forward(self, x):
    #apply linear layer and activation function
        x=F.relu(self.linear1(x))
    #no activation function needed at the end
        x=self.linear2(x)
        return x
    
    #create function to save the model later
    def save(self, file_name='model.pth'):
        model_folder_path ='./model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        
        file_name=os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
################END OF MODEL#########################

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr=lr
        self.model=model
        self.gamma=gamma
        self.optimiser = optim.Adam(model.parameters(), lr=self.lr)
        #loss function ( can probably not name it criterion)
        self.criterion=nn.MSELoss()

    def train_step(self,state,action, reward, next_state, done):
        #convert this tuple or list, to a pytorch tensor
        state=torch.tensor(state, dtype=torch.float)
        next_state=torch.tensor(next_state, dtype=torch.float)
        action=torch.tensor(action, dtype=torch.float)
        reward=torch.tensor(reward, dtype=torch.float)
        #if the above has multiple values then it's in the form (n,x) which is correct

        # want to be able to handle multiple sizes
        if len(state.shape)==1: #then we only have 1 dimension
            #want to reshape to (1,x) [1 is the number of batches]
            state= torch.unsqueeze(state, 0)
            next_state= torch.unsqueeze(next_state, 0)
            action= torch.unsqueeze(action, 0)
            reward= torch.unsqueeze(reward, 0)
            done=(done, )# convert to tuple

    #want to get predicted Q values with current model
    ## tutorial had = =
        pred = self.model(state)    
    #apply formular: Q_new= reward+ gamma * the MAX(next predicted Q value). #only do this if not done
    #pred.clone()
    #preds[argmax(action)] = Q-new
    # gets 1 value in to 2, 2 are cloned and action is new
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new= reward[idx]+ self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action).item()] = Q_new
        
        self.optimiser.zero_grad()  #empties the gradient
        loss =self.criterion(target, pred) #caluclates the loss
        loss.backward() # call back propogation

        self.optimiser.step()






