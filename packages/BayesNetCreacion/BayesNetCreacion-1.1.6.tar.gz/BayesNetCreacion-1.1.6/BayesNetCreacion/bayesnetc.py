# Base
class BayesNetCreacion():
    def __init__(self):
        """
        Class variables:
        :variables: List, Saves all the variables added to the network
        :parents: Dict, Saves all the parents of the variables added
        :cpt: Dict, contains alll the probabilities of the variables in the network
        """
        self.variables = ()
        self.parents = {}
        self.cpt = {}
    
    def add_node(self, node): #Adds node object to the network
        query = {str(node): node.get_parents()}
        self.parents.update(query)
        self.variables += tuple(query.keys())
    
    def add_prob(self, prob): #Adds a probability or cpt to the network
        self.cpt.update(prob)
    
    def get_network(self): #Returns a dict containing the network values
        return {
            'variables': self.variables,
            'parents': self.parents,
            'cpt' : self.cpt
        }

    def probabilistic_inference(self, query, evidence):
        """
        Calculate the probability of the query given the evidence inputted

        :param: query: the variable to calculate the prob for
        :param: evidence: the evidence, given a dictionary with their values
        :return: the probability of the query happening given the evidence
        """
        result = self.pre_enum(query, evidence)
        return result[True]

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

    #Additional services



    def get_factors(self): #Returns factors of the network (dict)
        return self.cpt

    def pre_enum(self, X, e): 
        QX = {}
        for xi in [True, False]:
            e[X] = xi
            QX[xi] = self.get_enum(self.variables, e)
        return self.normalize(QX)
    
    def get_enum(self, variables, e): #Returns numeration value(s)
        if not variables:
            return 1
        Y, rest = variables[0], variables[1:]
        if Y in e:
            return self.P(Y, e) * self.get_enum(rest, e)
        else:
            return sum(self.P(Y, self.extend(e, Y ,yi))* self.get_enum(rest, self.extend(e, Y, yi))
                        for yi in [True, False])

    def extend(self, e, var, val):
        e2 = dict(e)
        e2[var] = val
        return e2

    def normalize(self, QX): #Returns the normalized numeration value
        total = sum(QX.values())
        for key in QX:
            QX[key] /= total
        return QX


#Creation of each probabilistic node that will form the network
class Node():
    def __init__(self, name):
        """
        Class variables:
        :name: String, contains the name which identifies the node created.
        :parents: String list, contains the names of the parents of the node, is empty if node doesnt have parents.
        """
        self.name = name
        self.parents = [] 
    
    def __str__(self):
        return self.name

    def set_parents(self, parents: list):
        self.parents = parents
    
    def get_parents(self):
        return self.parents
    
    

