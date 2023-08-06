from collections import defaultdict

class BayesianNetwork:
    def __init__(self, parents, cpt):
        """
        Initialize the Bayesian network with a dictionary of parents and a dictionary of conditional probability tables.

        :param variables: a list containing each variable from parents
        :param parents: a dictionary that maps each variable to its parent variables
        :param cpt: a dictionary that maps each variable-value pair and its parent variables-values to its probability
        """
        self.variables = list(parents.keys())
        self.parents = parents
        self.cpt = cpt

    def P(self, var, e):
        """
        Calculate the probability of a variable given its parents in the network, using the conditional probability table.

        :param var: the variable to calculate the probability for
        :param e: the evidence, a dictionary that maps variables to their values
        :return: the probability of the variable given the evidence
        """
        
        key = (var, e[var])
        for p in self.parents[var]:
            key += tuple(p)
            key += tuple([e[p]])
        return self.cpt[key]

def enumeration_ask(X, e, bn):
    QX = {}
    for xi in [True, False]:
        e[X] = xi
        QX[xi] = enumerate_all(bn.variables, e, bn)
    return normalize(QX)

def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    Y, rest = variables[0], variables[1:]
    if Y in e:
        return bn.P(Y, e) * enumerate_all(rest, e, bn)
    else:
        return sum(bn.P(Y, extend(e, Y, yi)) * enumerate_all(rest, extend(e, Y, yi), bn)
                   for yi in [True, False])

def extend(e, var, val):
    e2 = dict(e)
    e2[var] = val
    return e2

def normalize(QX):
    total = sum(QX.values())
    for key in QX:
        QX[key] /= total
    return QX

# Define the Bayesian network
network = BayesianNetwork({
    'B': [],
    'E': [],
    'A': ['B', 'E'],
    'J': ['A'],
    'M': ['A']
}, {
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

# Perform probabilistic inference
evidence = {'J': True, 'M': True}
query = 'B'
result = enumeration_ask(query, evidence, network)
print(result[True])

