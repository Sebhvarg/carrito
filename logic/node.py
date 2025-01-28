class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
     

    
