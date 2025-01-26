class Edge:
    def __init__(self, source, target, weight =1):
        self.source = source
        self.target = target
        self.weight = weight
        
    def __str__(self):
        return f"{self.source} -> {self.target} : {self.weight}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __hash__(self):
        return hash((self.source, self.target))