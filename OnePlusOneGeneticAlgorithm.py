import random
import numpy
from CandidateSolution import CandidateSolution




def improve_by_mutation(cs: CandidateSolution, mutation_rate) -> CandidateSolution:
    rate = mutation_rate
    mutated = [ (1-x) if random.random() < rate else x for x in cs.genotype ]
    new_cs = CandidateSolution(genotype=mutated, fitness_evaluator=cs.fitness_evaluator)
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs

def improve_by_reset(cs: CandidateSolution, mutation_rate) -> CandidateSolution:
    new_cs = CandidateSolution(length=len(cs.genotype), fitness_evaluator=cs.fitness_evaluator)
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs

def improve_by_tabu_reset(cs: CandidateSolution, mutation_rate) -> CandidateSolution:
    fiteval = cs.fitness_evaluator
    keep_going = True
    while keep_going: 
        #print(".", end="")
        new_cs = CandidateSolution(length=len(cs.genotype), fitness_evaluator=fiteval)
        key = tuple(new_cs.genotype)
        if key not in fiteval.fitness_cache.keys():
            break
    #print()
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs


def evolve( max_iterations, geno_size, improve_method=None, mutation_rate=None, fitness_evaluator=None):  
    cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
    cs.evaluate()
    improve_functions = { 
        "by_reset":         improve_by_reset,
        "by_mutation":      improve_by_mutation,
        "by_tabu_reset":    improve_by_tabu_reset
    }
    improve = improve_functions[improve_method]
    for iteration in range(max_iterations):
        cs = improve(cs, mutation_rate)
        if cs.fitness >= fitness_evaluator.max_fitness:
            break
    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (cs.fitness, iteration) + cache_usage
