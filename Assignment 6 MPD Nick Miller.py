###MDP assignment
###Programmed by: Nick Miller
###Assistance by: Alex Cody
###Alex helped me print the U values and the policy properly-
import random
class MDP:
    def __init__(self):
        self.states = [0]*16
        self.discount = .95
        for i in range(16):
            self.states[i] = i 
            
        self.actions = [0,1,2,3]  #Actions [Up,down,left,right] as suggested in the right up
        #creating the reward function
        self.reward = [0]*len(self.states) 
        for i in range(16):
            if(i==12):
                self.reward[i] = 200 
            elif(i==10):
                self.reward[i] = 100 
            elif(i%2==1): #odd numbers get 50, even numbers stay at 0
                self.reward[i] = 50 
        ##Creating a 3D array for the transition function
        ##Then writing all of the probabilities
        self.transition = [[[0.0 for i in range(len(self.actions))] for i in range(len(self.states))] for i in range(len(self.states))] 
        for states in self.states:
            for action in self.actions:
                #next state if action succeeds
                sprime = 0 
                if(action==0):
                    sprime = states + 4 
                elif(action==1):
                    sprime = states - 4 
                elif(action==2):
                    sprime = states - 1 
                elif(action==3):
                    sprime = states + 1 
                if(sprime>=0 and sprime<len(self.states)):
                    if(not(action==2 and states%4==0) and not(action==3 and states%4==3)):
                        self.transition[sprime][states][action] += .7 
                else:
                    if(action==0):
                        self.transition[states-4][states][action] += .7
                    elif(action==1):
                        self.transition[states+4][states][action] += .7 
                    elif(action==2 and states%4!=0):
                        self.transition[states+1][states][action] += .7 
                    elif(action==3 and states%4!=3):
                        self.transition[states-1][states][action] += .7 
                
                #next state if the action will not work
                sprime = 0 
                if(action==0):
                    sprime = states - 4 
                elif(action==1):
                    sprime = states + 4 
                elif(action==2):
                    sprime = states + 1 
                elif(action==3):
                    sprime = states - 1 
                if(sprime>=0 and sprime<len(self.states)):
                    #Checking for a valid move
                   if(not(action==2 and states%4==3) and  not(action==3 and states%4==0)):
                       self.transition[sprime][states][action] += .2 
                else:
                    if(action==0):
                        self.transition[states+4][states][action] += .2 
                    elif(action==1):
                        self.transition[states-4][states][action] += .2 
                    elif(action==2):
                        self.transition[states-1][states][action] += .2 
                    elif(action==3):
                        self.transition[states+1][states][action] += .2 

                #next state if there is no move
                #sprime = states in this case
                sprime = states
                self.transition[sprime][states][action] += .1 
                
    def ValueIteration(self,maxError):
        U = [0]*len(self.states)
        Uprime = [0]*len(self.states)
        discount = .95
        while(True):
            #copy u1 to u
            for s in range(len(Uprime)):
                U[s] = Uprime[s] 
            delta = 0
            #Computing the sums 
            for state in range(len(self.states)):
                sumOverActions = [0]*len(self.actions) 
                for action in range(len(self.actions)):
                    sumOverActions[action] = 0 
                    for sprime in range(len(self.states)):
                        sumOverActions[action] += self.transition[sprime][state][action] * U[sprime] 
                Uprime[state] = self.reward[state] + self.discount * max(sumOverActions) 
                delta = max(delta,abs(Uprime[state]-U[state])) 
            if(delta<((maxError*(1.0-self.discount))/self.discount)):
                break 
        
        #obtain my optimal policy
        policy = [0]*len(self.states)
        for states in range(len(self.states)):
            policy[states] = 0
            valueOfActions = [0]*len(self.actions)
            for action in range(len(self.actions)):
                valueOfActions[action] = 0
                for sprime in range(len(self.states)):
                    valueOfActions[action] += self.transition[sprime][states][action] * U[sprime]
            policy[states] = valueOfActions.index(max(valueOfActions))
        return policy,U

    def PolicyIteration(self,iterations):
        U = [0]*len(self.states) 
        policy = [0]*len(self.states) 
        for s in range(len(self.states)):
            policy[s] = 2
        unchanged = False 
        while(not unchanged):
            for k in range(1,iterations):
                for s in range(len(self.states)):
                    total = 0 
                    for s1 in range(len(self.states)):
                        
                        total += self.transition[s1][s][policy[s]]*U[s1] 
                    U[s] = self.reward[s] + self.discount * total 

            #Now that I have U, I can find the optimal policy
            #If I find the optimal policy, I will break out of the loop
            #If I don't, based on the last if statement, I will remain in the loop
            unchanged = True 
            for state in range(len(self.states)):
                sumOverActions = [0]*len(self.actions) 
                for action in range(len(self.actions)):
                    for sprime in range(len(self.states)):
                        sumOverActions[action] += self.transition[sprime][state][action] * U[sprime] 
                maxA = max(sumOverActions) 
                bestA = sumOverActions.index(maxA) 
                if maxA > sumOverActions[policy[state]]:
                    policy[state] = bestA 
                    unchanged = False 
        return policy,U 
    def printPolicy(self,actions):
        #Will print the policies nicely, using characters to represent direction
        toPrint = "" 
        for i in range(len(actions)-1,-1,-1):
            if i%4==3:
                toPrint += "\n" 
            if(actions[i]==0):
                toPrint += " ^ " 
            elif(actions[i]==1):
                toPrint += " v " 
            elif(actions[i]==2):
                toPrint += " < " 
            elif(actions[i]==3):
                toPrint += " > " 
        print toPrint 

    def printValueFunction(self,utilities):
        ##Will print the utility nicely
        toPrint = "" 
        for i in range(len(utilities)-1,-1,-1):
            if i%4==3:
                toPrint += "\n" 
            toPrint += " " + `int(round(utilities[(4*abs((3-i)/4))+(3-(i%4))]))` + " " 
        print toPrint 
                                           
def main():
    mdp = MDP() 

    valueIteration = mdp.ValueIteration(pow(10,-10)) 
    actionarray = valueIteration[0] 
    utilityarray = valueIteration[1] 
    
    mdp.printValueFunction(utilityarray) 
    print "" 
    mdp.printPolicy(actionarray) 
    
    policyIteration = mdp.PolicyIteration(100) 
    actionarray = policyIteration[0] 
    utilityarray = policyIteration[1] 
    
    mdp.printValueFunction(utilityarray) 
    print "" 
    mdp.printPolicy(actionarray) 
    
main() 
