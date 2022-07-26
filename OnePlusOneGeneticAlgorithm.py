import random
import numpy
from CandidateSolution import CandidateSolution




def improve(cs: CandidateSolution) -> CandidateSolution:
    if cs.fitness is None:
        cs.evaluate()
    #rate = 1/len(cs.genotype)
    rate = 0.5
    mutated = [ (1-x) if random.random() < rate else x for x in cs.genotype ]
    new_cs = CandidateSolution(genotype=mutated, fitness_evaluator=cs.fitness_evaluator)
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs




def evolve( max_iterations, geno_size, fitness_evaluator=None):    
    pop = []
    cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
    cs.evaluate()
    pop.append(cs)
    
    for iteration in range(max_iterations):
        os = improve(cs)
        if os.fitness >= cs.fitness:
            cs = os
        if cs.fitness >= fitness_evaluator.max_fitness:
            break

    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (cs.fitness, iteration) + cache_usage

