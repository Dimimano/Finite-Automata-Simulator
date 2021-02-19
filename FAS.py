import linecache
import sys
import copy

#Ask user to input the file path.
print('Please enter the file path (e.g. "C:\workspace\Automaton.txt"). \n')
FilePath = input()

#Every line in the file has different information about the automaton. Each iteration, a different line is examined so its needed to track the line we currently look at.   
iterationCounter = 1

#Start reading on the file's first line.
currentLine = 1

#List for saving the automaton's states.
stateList = []

#List for saving the automaton's current states.
currentStateList = []

#If the automaton contains e-transitions this boolean variable becomes 1.
eTransitions = 0

while(1):
    #Read the first line
    retrieved_line_with_spaces = linecache.getline(FilePath, currentLine)
    
    #Remove spaces
    retrieved_line_1 = retrieved_line_with_spaces.replace(" ","")
    retrieved_line = retrieved_line_1.replace("\n","")
    #1st line contains the amount of states.
    if iterationCounter == 1:
        #Create a state, numbered from 1 to N where N is the amount of states and save them in the list.
        for state in range(1,int(retrieved_line)+1):
            stateList.append(state)
        iterationCounter += 1
        currentLine += 1 
        continue 

    #2nd line contains the starting state's number
    elif iterationCounter == 2:
        #Save the starting state as the first current state.
        currentStateList.append(retrieved_line)
        startingState = retrieved_line
        iterationCounter += 1
        currentLine += 1
        continue
    
    #3rd line contains the amount of accepting states
    elif iterationCounter == 3:
        amountOfAcceptStates =  retrieved_line
        iterationCounter += 1
        currentLine += 1
        #Create the list that contains each accepting state
        acceptStateList = []
        for x in range(int(amountOfAcceptStates)):
            acceptStateList.append(' ')
        continue
    
    
    
    #4th line contains the accepting state's number   
    elif iterationCounter == 4:
        #Append the numbers of states that are accepting states.
        if retrieved_line[0] == ',':
            i=1
            j=0
            while(int(retrieved_line[i]) >= 0):
                endOfState1 = retrieved_line.find(',', i)
                for i in range(i,endOfState1):
                        acceptStateList[j] = str(acceptStateList[j]) + retrieved_line[i]
                i = i+2
                j = j+1
                if i>len(retrieved_line)-1:
                    iterationCounter += 1
                    currentLine += 1
                    break
            continue
        else:
            for state in retrieved_line:
                acceptStateList.append(state)
            iterationCounter += 1
            currentLine += 1
            continue
    
    #5th line contains the amount of transitions
    elif iterationCounter == 5:
        #Tx3 List (nested lists) for saving the automaton's transitions.
        #T is the amount of transitions, on the 1st column the state's number is saved, on the 2nd column the letter that defines the transition is saved
        #and in the 3rd column, the state's number which is pointed at is saved.
        transitionsAmount = retrieved_line
        transitionStateList = [[0 for x in range(3)] for y in range(int(transitionsAmount))]
        iterationCounter += 1
        currentLine += 1
        continue
       
    #The rest of the lines contain the transitions between the states which are saved in the 2D list.
    elif iterationCounter > 5:
        #If the line is not empty
        if retrieved_line:
            #If the first character in a line is the comma (,) then the automaton has more than 9 states
            #  and this line contains a transition from or to a state that is defined from a number higher than 9.
            if retrieved_line[0] != ',':
                rowIndex = iterationCounter-6
                transitionStateList[rowIndex][0] = retrieved_line[0]
                transitionStateList[rowIndex][1] = retrieved_line[1]
                transitionStateList[rowIndex][2] = retrieved_line[2]
                iterationCounter += 1
                currentLine += 1
                
            #In the case of the automaton with more states than 9 it is impossible to know how many digit does the number which 'defines' a state may contain.
            #We ask the user to enclose them in commas in order to know where they start/end.
            if retrieved_line[0] == ',':
                rowIndex = iterationCounter-6
                endOfState1 = retrieved_line.find(',', 1)
                for i in range(1,endOfState1):
                    if str(transitionStateList[rowIndex][0]) != '0':
                        transitionStateList[rowIndex][0] = str(transitionStateList[rowIndex][0]) + retrieved_line[i]
                    if str(transitionStateList[rowIndex][0]) == '0':
                        transitionStateList[rowIndex][0] = retrieved_line[i]
                transitionStateList[rowIndex][1] = retrieved_line[endOfState1+1]
                if retrieved_line[endOfState1+1] == '@':
                    eTransitions = 1
                endOfState2 = retrieved_line.find(',', endOfState1+3)
                for i in range(endOfState1+3,endOfState2):
                    if str(transitionStateList[rowIndex][2]) != '0':
                        transitionStateList[rowIndex][2] = str(transitionStateList[rowIndex][2]) + retrieved_line[i] 
                    if str(transitionStateList[rowIndex][2]) == '0':
                        transitionStateList[rowIndex][2] = retrieved_line[i] 
                iterationCounter += 1
                currentLine += 1
                
            #If an '@' is found we know the automaton contains e-transitions.
            if retrieved_line[1] == '@':
                eTransitions = 1
           
        #If the line is empty stop reading the file.
        else:
            break

#Remove empty characters inside of the state's number.
for i in range(0,len(acceptStateList)):
    acceptStateList[i] = acceptStateList[i].replace(" ","")       
     
#After testing a word through the automaton the currentState List is changed so the original starting currentState List needs to be saved.
currentStateListOriginal = currentStateList

#The automaton's transition function, returns the updated list that contains the current states.       
def transitionFunction(letter,startingState,acceptStateList,currentStateList,transitionStateList,transitionsAmount):
    temporary_current_List = []
    
    #Search the transitions based on the current letter which is examined and the current states and update the temporary current list accordingly.
    for state in currentStateList:
        for i in range(0,int(transitionsAmount)):
            if transitionStateList[i][0] == state and transitionStateList[i][1] == letter:
                temporary_current_List.append(transitionStateList[i][2])  
    
    #If the temporary current list got updated the automaton continues reading letters.
    if len(temporary_current_List) != 0:
        stop = 0 
        return temporary_current_List,stop
    
    #If the temporary current list is empty, the automaton either read an empty word or a letter that there is no transition for from a current state.
    #Note: the empty word for this simulation is defined as " " (spacebar).
    elif len(temporary_current_List) == 0:
        
        #If the word is empty and the starting state is also an accepting state then stop reading more letters and accept the word.
        if letter == ' ' and startingState in acceptStateList:
            stop = 1
            return temporary_current_List,stop
        if letter == ' ' and startingState not in acceptStateList:
            stop = 0
            return temporary_current_List,stop
        
        #If the word is not empty it means the automaton read a letter that there is no transition for from a current state.
        #Return an empty list as the new accept list in order for the word to not be accepted.
        if letter != ' ':
            stop = 0
            return temporary_current_List,stop

#If the automaton contains e-transitions this function produces a new transitions list that defines the same automaton without e-transitions.    
def convertToNoEpsilon(acceptStateList,transitionStateList,transitionsAmount):
    
    transitionsAmount_before = transitionsAmount
    acceptStateList_before = b = copy.deepcopy(acceptStateList)
    #An alphabet is a set so this is the data structure used in order to save it.
    alphabet = set()
    for i in range(0,int(transitionsAmount)):
        if transitionStateList[i][1] != '@':
            alphabet.add(transitionStateList[i][1])
    
    #After the set is created, convert to a list in order to be able to index it. Sort it and add the e-transitions character. 
    alphabet_list = list(alphabet)
    alphabet_list.sort()
    alphabet_list.append('@')
    
    #The E_transition_Matrix has as many lines as the amount of the automaton's state and as many columns as the alphabet's length plus an extra column for the e-transitions.
    E_transition_Matrix = [[' ' for x in range(len(alphabet)+1)] for y in range(len(stateList))]
    
    #The following triple loop essentially reads the transitionStateList and tranforms it to the E_transition_Matrix which later is used in order to create each state's E_Closure list.
    for i in range(1,len(stateList)+1):
        for j in range(0,int(transitionsAmount)):
            for letter in alphabet_list:
                if transitionStateList[j][0] == str(i) and transitionStateList[j][1] == letter:
                    rowIndex = int(transitionStateList[j][0]) - 1
                    columnIndex = alphabet_list.index(letter)
                    if E_transition_Matrix[int(rowIndex)][columnIndex] == ' ':
                        E_transition_Matrix[int(rowIndex)][columnIndex] = E_transition_Matrix[rowIndex][columnIndex]  + transitionStateList[j][2]
                    elif E_transition_Matrix[int(rowIndex)][columnIndex] != ' ':
                        E_transition_Matrix[int(rowIndex)][columnIndex] = E_transition_Matrix[rowIndex][columnIndex] + ',' + transitionStateList[j][2]
    print('Transitions List: ',transitionStateList,'\n')
    print('E Transition Matrix: ',E_transition_Matrix,'\n')
    #The E_Closure matrix has is a square matrix that has as many lines and columns as the amount of the automaton's state.
    #Each state has its own line in the matrix which contains the states that is possible to go to using a e-transition plus the state itself.                            
    E_closure = [[' ' for x in range(len(stateList))] for y in range(len(stateList))]
    
    #Using the column in the E_transition_Matrix which contains every state's possible e-transitions the E_Closure matrix is created.
    for i in range(0,len(stateList)):
        x=E_transition_Matrix[i][len(alphabet)].replace(" ","")
        if len(x)>1 and ',' not in x:
            E_closure[i][0] = str(stateList[i])
            E_closure[i][1] = x
            continue
        for j in range(0,len(stateList)-1):
            listEClosureStates = list(E_transition_Matrix[i][len(alphabet)])
            listEClosureStates = [x for x in listEClosureStates if len(x.strip()) > 0]
            for b in range(0,len(listEClosureStates)-1):
                if listEClosureStates[b] == ',':
                    listEClosureStates.pop(b)
                    
            E_closure[i][0] =  str(stateList[i])
            if j <= len(listEClosureStates) and j>0:
                E_closure[i][j] = listEClosureStates[j-1]
                x=1
                y=j+1
                rowIndex = int(listEClosureStates[j-1])-x
                columnIndex = alphabet_list.index('@')
                while(E_transition_Matrix[rowIndex][columnIndex] != ' '):
                    helper = list(E_transition_Matrix[rowIndex][columnIndex])
                    for z in range(0,len(helper)-1):
                        if helper[z] == ',':
                            helper.pop(z)
                    helper = [x for x in helper if len(x.strip()) > 0]
                    for a in range(0,len(helper)):
                        E_closure[i][y] = E_closure[i][y] + helper[a]
                        y += 1
                    x -= 1
                    y += 1
                    rowIndex = int(listEClosureStates[j-1])-x
    print('E_Closure Matrix: ',E_closure,'\n')
    #After creating the E_transition_Matrix and the E_Closure matrix it now possible to create the no_E_transition_Matrix.
    #This matrix, as in the case of the E_transition_Matrix, has a line for every state and a column for every letter in the alphabet but no e-transition column.
    #Using the E_Closure matrix the function knows which of the E_transition_Matrix's lines to add in order to create the no_E_transition_Matrix.
    no_E_transition_Matrix = [[' ' for x in range(len(alphabet))] for y in range(len(stateList))]
    for i in range(0,len(stateList)):
        for j in range(0,len(E_closure[i])):
            if E_closure[i][j] != ' ':
                if int(E_closure[i][j]) == i+1:
                    for x in range(0,len(alphabet)):
                        no_E_transition_Matrix[i][x] = E_transition_Matrix[i][x]
                else: 
                    for x in range(0,len(alphabet)):
                        rowIndex = stateList.index(int(E_closure[i][j]))
                        no_E_transition_Matrix[i][x] =E_transition_Matrix[rowIndex][x] + no_E_transition_Matrix[i][x]
    print('No E Transition Matrix: ',no_E_transition_Matrix,'\n')
    #In the final step, the function reads every line of the no_E_transition_Matrix and accordingly creates the new_Transitions_list that doesn't contain e-transitions.
    #The new_Transitions_list essentially defines a No e-transitions NDA and can be used from transitionFunction above as it is.
    z=0
    new_Transitions_list = [[' ' for x in range(3)] for y in range(len(stateList)*len(alphabet))]
    for i in range(0,len(stateList)):
        for j in range(0,len(alphabet)):
            listOfStates = list(no_E_transition_Matrix[i][j])
            listOfStates = [x for x in listOfStates if len(x.strip()) > 0]
            for x in range(0,len(listOfStates)):
                if listOfStates[x] != ' ':
                    new_Transitions_list[z][0] = str(stateList[i])  
                    new_Transitions_list[z][1] = str(alphabet_list[j])
                    if len(listOfStates) > 1 and x<= len(listOfStates)-2 :
                        if int(listOfStates[x] + listOfStates[x+1]) <= len(stateList):
                            new_Transitions_list[z][2] = str(int(listOfStates[x] + listOfStates[x+1]))
                            z += 1
                            break
                    new_Transitions_list[z][2] = str(listOfStates[x])
                    z += 1
    print('New Transition List: ',new_Transitions_list,'\n')                
    #The transitions amount need to be updated as well as the accepting states. Every state that can get to an accepting state with e-transitions becomes an accepting state as well.
    i=0           
    while(i<=len(new_Transitions_list)-1):
        if new_Transitions_list[i] == [' ', ' ', ' ']:
            new_Transitions_list.remove(new_Transitions_list[i])
            i=i-1
        i=i+1
    transitionsAmount = len(new_Transitions_list)
    for i in range(0,len(stateList)):
        for j in range(0,len(stateList)):
            string = E_closure[i][j].replace(" ", "")
            if string in acceptStateList and str(stateList[i]) not in acceptStateList:
                acceptStateList.append(str(stateList[i]))
    acceptStateList = list(dict.fromkeys(acceptStateList)) 
    print('Transition Amount before: ',transitionsAmount_before, ' Transitions Amount now: ',transitionsAmount,'\n')
    print('Accept List before: ',acceptStateList_before,' New Accept State List: ',acceptStateList,'\n')
    return new_Transitions_list,acceptStateList,transitionsAmount
                
                
            
#If there are e-transitions the conversion happens once at the start no matter how many words the user inputs.    
ConvertOnce = 1

#In this while loop, the program is interacting with the user, who inputs words he wants to check.
while(1):
    
    print('Please enter a word. \n')
    word = input()
    
    #Convert the word into a list which containts its letters.
    listWord = list(word)
    
    #If e-transitions exist convert once.
    if ConvertOnce and eTransitions:
        transitionStateList,acceptStateList,transitionsAmount = convertToNoEpsilon(acceptStateList,transitionStateList,transitionsAmount)
    ConvertOnce = 0
    
    #Using the word, call the transition function for each of the word's letters.
    for letter in listWord:
        currentStateList,stop = transitionFunction(letter,startingState,acceptStateList,currentStateList,transitionStateList,transitionsAmount)
        if stop == 1:
            break  
        
    #When the transition function finishes updating the current states, if at least one the current states is an accepting state the word is accepted.
    accept = 0
    
    for state in currentStateList:
        if state in acceptStateList:
            accept = 1
            
    if stop:
        accept = 1
    if accept:
        print('The word is accepted by the automaton')
    else:
        print('The word is not accepted by the automaton')
    
    #Interacting with the user in order to keep testing words or end the script.    
    print('Do you want to test more words? [Y,N] \n')
    answer_caps = input()
    answer = answer_caps.upper()
    if answer == 'Y':
        currentStateList = currentStateListOriginal
        continue 
    elif answer == 'N':
        sys.exit()
    else:
        print('[Y,N] are the only valid asnwers. Script shutting down.')
        sys.exit()   