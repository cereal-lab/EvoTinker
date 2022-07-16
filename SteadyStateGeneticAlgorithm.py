from random import choice
from random import sample
from random  import randint
from random import random

from dataclasses import dataclass


class FitnessEvaluator(object):
    
        
    def __init__(self):
        #pass # if we init fields here, the constructor is run everytime we create a singleton
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache = {}
            
    def evaluate(self, genotype):
        key = tuple(genotype)
        #print("Evaluating", self.cache_hits, self.cache_misses)
        if key in self.fitness_cache.keys():
            self.cache_hits += 1
            return self.fitness_cache[key]
        else:
            self.cache_misses += 1
            fitness_value = self.OneMax(genotype)
            self.fitness_cache[key] = fitness_value
            #print("after", self.fitness_cache)
            return fitness_value
    
    def report_cache_usage(self):
        return (self.cache_hits , self.cache_misses)
    
    def zero_cache_usage(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache.clear()
    
    def OneMax(self, genotype):
        return sum(genotype)
    
    ##def __new__(cls):
    ##    # implements singleton pattern
    ##    # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    ##    if not hasattr(cls, 'instance'):
    ##      cls.instance = super(FitnessEvaluator, cls).__new__(cls)
    ##    return cls.instance


fitness_evaluator = FitnessEvaluator()


class CandidateSolution(object):
    
    def __init__(self, length=None, genotype=None):
        if genotype is None:
            self.genotype = []
            for _ in range(length):
                self.genotype.append(randint(0,1))
        else:
            self.genotype = genotype
        self.fitness = None
        
    def evaluate(self):
        #self.fitness = FitnessEvaluator().evaluate(self.genotype)
        self.fitness = fitness_evaluator.evaluate(self.genotype)
    
    def __repr__(self):
        return f"<{self.genotype}>"




def recombine(p1: CandidateSolution, p2: CandidateSolution):
    mask = [0 if random() < 0.5 else 1 for _ in range(len(p1.genotype))]
    os1 = [p1.genotype[i] if mask[i] == 0 else p2.genotype[i]
           for i in range(len(mask))]
    os2 = [p1.genotype[i] if mask[i] == 1 else p2.genotype[i]
           for i in range(len(mask))]
    return os1,os2




def mutate(cs, rate=None):
    if rate is None:
        rate = 1/len(cs)
        #rate = randint(1,len(cs)//4)/len(cs)
    return [x if random() >= rate else (1-x) for x in cs ]




def replace_OLD(pop, cs):
    smallest = min(pop, key=lambda item: item.fitness)
    #pop = [x for x in pop if x.fitness > smallest else cs]
    newpop = []
    already_replaced = False
    for i in range(len(pop)):
        if pop[i].fitness > smallest.fitness or already_replaced:
            newpop.append(pop[i])
        else:
            already_replaced = True
            newpop.append(cs)
    return newpop

def replace(pop, cs):
    smallest = min(pop, key=lambda item: item.fitness)
    for i in range(len(pop)):
        if pop[i].fitness == smallest.fitness:
            break
    pop.pop(i)
    pop.append(cs)
    return pop




def select(p, kt=2):
    pool = sample(p,k=kt)
    return max(pool, key=lambda item: item.fitness)




def diversify(p: list):
    #hypermutation wannabe
    #for _ in range(pop_size // 5):
    #    new_cs = CandidateSolution(geno_size)
    #    new_cs.evaluate()
    #    pop = replace(pop, new_cs)
    for _ in range(len(p) // 10):
        new_cs = CandidateSolution(genotype=list(choice(list(fitness_evaluator.fitness_cache))))
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p
        




def evolve(max_iterations, pop_size, kt, geno_size):
    pop = []
    for _ in range(pop_size):
        pop.append(CandidateSolution(geno_size))
    for i in range(pop_size):
        pop[i].evaluate()
        
    best = max(pop, key=lambda item: item.fitness)
    #print(f"Iteration #0:", best.fitness)

    for iteration in range(max_iterations):
        p1 = select(pop, kt)
        p2 = select(pop, kt)

        os1, os2 = recombine(p1,p2)

        os1 = mutate(os1)
        os2 = mutate(os2)

        cs1 = CandidateSolution(genotype=os1)
        cs2 = CandidateSolution(genotype=os2)
        cs1.evaluate()
        cs2.evaluate()
        
        #pop = diversify(pop)
        
        pop = replace(pop, cs1)
        pop = replace(pop, cs2)

        best = max(pop, key=lambda item: item.fitness)
        #print(f"Iteration #{iteration}:", best.fitness)

    print("\nBest Candidate Solution:", best.fitness)
    #print("FitnessCache usage:", FitnessEvaluator().report_cache_usage())
    print("FitnessCache usage:", fitness_evaluator.report_cache_usage())
    #FitnessEvaluator().zero_cache_usage()
    #print(fitness_evaluator.fitness_cache)
    fitness_evaluator.zero_cache_usage()


if __name__ == '__main__':
    #evolve(geno_size=100, max_iterations=400, pop_size=25, kt=2)
    evolve(geno_size=1000, max_iterations=4000, pop_size=25, kt=2)
