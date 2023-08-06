from BayesNetCreacion import BayesNetCreacion, Node

#Burglar Alarm System example 
#Reference: https://www.youtube.com/watch?v=hEZjPZ-Ze0A&t=35s

#Creating nodes and network
burglary = Node('B')
earthquake = Node('E')
alarm = Node('A')
johncalls = Node('J')
marycalls = Node('M')

alarm.set_parents([str(burglary),str(earthquake)])
johncalls.set_parents([str(alarm)])
marycalls.set_parents([str(alarm)])

bnc = BayesNetCreacion()
bnc.add_node(burglary)
bnc.add_node(earthquake)
bnc.add_node(alarm)
bnc.add_node(johncalls)
bnc.add_node(marycalls)

bnc.add_prob({
    ('B', True): 0.001,
    ('B', False): 0.999,
    ('E', True): 0.002,
    ('E', False): 0.998,
    ('A', True, 'B', True, 'E', True): 0.95,
    ('A', True, 'B', False, 'E', True): 0.29,
    ('A', True, 'B', True, 'E', False): 0.94,
    ('A', True, 'B', False, 'E', False): 0.001,
    ('A', False, 'B', True, 'E', True): 0.05,
    ('A', False, 'B', False, 'E', True): 0.71,
    ('A', False, 'B', True, 'E', False): 0.06,
    ('A', False, 'B', False, 'E', False): 0.999,
    ('J', True, 'A', True): 0.9,
    ('J', True, 'A', False): 0.05,
    ('J', False, 'A', True): 0.1,
    ('J', False, 'A', False): 0.95,
    ('M', True, 'A', True): 0.7,
    ('M', True, 'A', False): 0.01,
    ('M', False, 'A', True): 0.3,
    ('M', False, 'A', False): 0.99,
})

# print(bnc.get_network())

#Functions
#Probabilistic Inference
evidence = {'J': True, 'M': True}
query = 'B'
result = bnc.probabilistic_inference(query, evidence)
print(result) #0.28417

#Compact


#Factores
print(bnc.get_factors()) #Outputs Conditional Probability Table

#Definition check


#Enumeration
evidence = {'B': True, 'E':False}
query = 'A'
result = bnc.pre_enum(query, evidence)
print(result) #{True: 0.94, False: 0.06}