import random
import numpy
from FitnessEvaluator import FitnessEvaluator




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
        
    def evaluate(self):
        #self.fitness = FitnessEvaluator().evaluate(self.genotype)
        self.fitness = self.fitness_evaluator.evaluate(self.genotype)
    
    def __repr__(self):
        return f"<{self.genotype}>"




def recombine(p1: CandidateSolution, p2: CandidateSolution, rate=None):
    if rate is not None and random.random() < rate:
            mask = [0 if random.random() < 0.5 else 1 for _ in range(len(p1.genotype))]
            os1 = [p1.genotype[i] if mask[i] == 0 else p2.genotype[i]
                for i in range(len(mask))]
            os2 = [p1.genotype[i] if mask[i] == 1 else p2.genotype[i]
                for i in range(len(mask))]
            return os1,os2
    else:
        return p1.genotype, p2.genotype




def mutate(cs, rate=None):
    if rate is None:
        rate = 1/len(cs)
        #rate = random.randint(1,len(cs)//4)/len(cs)
        return [ (1-x) if random.random() < rate else x for x in cs ]
    else:
        if rate == -1:
            rate = numpy.random.power(5.0)
        return [ (1-x) if random.random() < rate else x for x in cs ]




def replace(pop, cs):
    smallest = min(pop, key=lambda item: item.fitness)
    for i in range(len(pop)):
        if pop[i].fitness == smallest.fitness:
            break
    pop.pop(i)
    pop.append(cs)
    return pop




def select(p, kt=2):
    pool = random.sample(p,k=kt*2)
    mid = len(pool)//2
    pool1 = pool[:mid]
    pool2 = pool[mid:]
    p1 = max(pool1, key=lambda item: item.fitness)
    p2 = max(pool2, key=lambda item: item.fitness)
    return p1, p2


    
def diversify_random_immigrant(p: list, fitness_evaluator: FitnessEvaluator):
    #random immigrant wannabe below:
    for _ in range(len(p) // 5):
        new_cs = CandidateSolution(len(p[0].genotype), fitness_evaluator=fitness_evaluator)
        new_cs.evaluate()
        pop = replace(pop, new_cs)
    return p
    
def diversify_cached_random_immigrant(p: list, fitness_evaluator: FitnessEvaluator):
    # cached random immigrant below:
    for _ in range(len(p) // 10):
        new_cs = CandidateSolution(genotype=list(random.choice(list(fitness_evaluator.fitness_cache))), fitness_evaluator=fitness_evaluator)
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p
        



def evolve(max_iterations, pop_size, kt, geno_size, mutation_rate=None, crossover_rate=None, fitness_evaluator=None):
    
    pop = []
    for _ in range(pop_size):
        pop.append(CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator))
    for i in range(pop_size):
        pop[i].evaluate()
        
    best = max(pop, key=lambda item: item.fitness)

    for iteration in range(max_iterations):
        #    p1 = select_OLD(pop, kt)
        #    p2 = select_OLD(pop, kt)
        p1,p2 = select(pop, kt)

        os1, os2 = recombine(p1,p2, rate=crossover_rate)

        os1 = mutate(os1, rate=mutation_rate)
        os2 = mutate(os2, rate=mutation_rate)

        cs1 = CandidateSolution(genotype=os1, fitness_evaluator=fitness_evaluator)
        cs2 = CandidateSolution(genotype=os2, fitness_evaluator=fitness_evaluator)
        cs1.evaluate()
        cs2.evaluate()
        
        #pop = diversify_cached_random_immigrant(pop, fitness_evaluator)
        
        pop = replace(pop, cs1)
        pop = replace(pop, cs2)

        best = max(pop, key=lambda item: item.fitness)
        if best.fitness >= fitness_evaluator.max_fitness:
            break

    cache_usage = fitness_evaluator.report_cache_usage()
    #print(fitness_evaluator.fitness_cache)
    fitness_evaluator.zero_cache_usage()
    return (best.fitness, iteration) + cache_usage




