# Finite-Automata-Simulator

The software takes as input a text file that contains the description of an automaton and simulates its operation, asking the user for words he/she wants to check if they are accepted or not from the automaton.
There are 3 types of aytomatons the software supports: Deterministic Finite Aytomata, Nondeterministic Finite Automata and Nondeterministic Finite Automata with e-transitions. The first 2 types were very simple to create while the e-transitions were tough to implement. In order to solve this problem, whenever e-transitions are detected from the software, the automaton is converted to its no e-transitions version which can be either Deterministic or Nondeterministic and its operation is correctly simulated.
