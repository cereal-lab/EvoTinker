import random
import numpy
from CandidateSolution import CandidateSolution




def improve(cs: CandidateSolution, mutation_rate) -> CandidateSolution:
    rate = mutation_rate
    mutated = [ (1-x) if random.random() < rate else x for x in cs.genotype ]
    new_cs = CandidateSolution(genotype=mutated, fitness_evaluator=cs.fitness_evaluator)
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs




def evolve( max_iterations, geno_size, mutation_rate=None, fitness_evaluator=None):  
    cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
    cs.evaluate()
    for iteration in range(max_iterations):
        cs = improve(cs, mutation_rate)
        if cs.fitness >= fitness_evaluator.max_fitness:
            break
    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (cs.fitness, iteration) + cache_usage
