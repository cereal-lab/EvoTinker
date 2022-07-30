import random



class CandidateSolution(object):
    
    def __init__(self, length=None, genotype=None, fitness_evaluator=None):
        self.fitness_evaluator = fitness_evaluator

        if genotype is None:
            self.genotype = []
            for _ in range(length):
                self.genotype.append(random.randint(0,1))
        else:
            self.genotype = genotype
        self.fitness = None
        self.outcome = None
        
    def evaluate(self):
        self.fitness, self.outcome = self.fitness_evaluator.evaluate(self.genotype)
    
    def __repr__(self):
        return f"<{self.genotype}>"
