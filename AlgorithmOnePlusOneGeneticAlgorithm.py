import random
import numpy
from CandidateSolution import CandidateSolution
#----
from rich.progress import track
import time


def recombine(p1: CandidateSolution, p2: CandidateSolution, rate=None):
    if rate is not None and random.random() < rate:
            mask = [0 if random.random() < 0.5 else 1 for _ in range(len(p1.genotype))]
            os1 = [p1.genotype[i] if mask[i] == 0 else p2.genotype[i]
                for i in range(len(mask))]
            os2 = [p1.genotype[i] if mask[i] == 1 else p2.genotype[i]
                for i in range(len(mask))]
            os1 = CandidateSolution(genotype=os1, fitness_evaluator=p1.fitness_evaluator)
            os2 = CandidateSolution(genotype=os2, fitness_evaluator=p2.fitness_evaluator)
            return os1,os2
    else:
        return p1, p2




def cached_recombination(cs: CandidateSolution, rate=1.0, kt_size=2) -> CandidateSolution:
    # dig in the cache for 2 parents, perform Xc, keep best child if it beat original
    
    fiteval = cs.fitness_evaluator
    cache_as_list = list(fiteval.fitness_cache)
    #print("Cache is ", len(cache_as_list))
    if len(cache_as_list) < kt_size: 
        #print("Not enough data in cache")
        return cs
    pool1 = random.sample(cache_as_list, kt_size)
    p1 = max(pool1, key=lambda genotype: fiteval.fitness_cache[tuple(genotype)])
    
    pool2 = random.sample(cache_as_list, kt_size)
    p2 = max(pool2, key=lambda genotype: fiteval.fitness_cache[tuple(genotype)])
    
    cs1 = CandidateSolution( genotype=p1, fitness_evaluator=fiteval)
    cs2 = CandidateSolution( genotype=p2, fitness_evaluator=fiteval)
    cs1.fitness = fiteval.fitness_cache[tuple(p1)]
    cs2.fitness = fiteval.fitness_cache[tuple(p2)]
    
    os1, os2 = recombine(cs1,cs2,rate)
    os1.evaluate()
    os2.evaluate()
    # the cache is our population, similar to archives
    alls = [cs, os1, os2] # NOTE do not include cs1 cs2
    best = max(alls, key=lambda item: item.fitness)
    best =  best if best.fitness >= cs.fitness else cs
    #print("Best is ", best.genotype)
    return best

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


def evolve( max_iterations, geno_size, 
            improve_method=None, 
            mutation_rate=None, 
            fitness_evaluator=None, 
            recombination=None, 
            experiment_number=None,
            experiment_total=None):  
    cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
    cs.evaluate()
    improve_functions = { 
        "by_reset":         improve_by_reset,
        "by_mutation":      improve_by_mutation,
        "by_tabu_reset":    improve_by_tabu_reset
    }
    improve = improve_functions[improve_method]
    
    if experiment_number != None and experiment_total != None: 
        descript = f'1+1GA {experiment_number:3d} /{experiment_total:3d}'
    else:
        descript = '1+1GA' 

    # NOTE: TODO: Pick an iterator: 
    it = track(range(max_iterations), description=descript) # for interactive shells
    # it = range(max_iterations) # for background batch jobs
    experiment_plot_best = []
    for iteration in it:
        #print(iteration)
        cs = improve(cs, mutation_rate)
        if recombination is not None:
            cs = cached_recombination(cs, rate=1.0, kt_size=recombination)
        # NOTE deactivate for TDO environments
        experiment_plot_best.append(cs.fitness)
        #if cs.fitness >= fitness_evaluator.max_fitness:
        #    break
    #print("------------")
    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (cs.fitness, iteration) + cache_usage + (experiment_plot_best,)
