import random
import numpy
from FitnessEvaluator import FitnessEvaluator
from CandidateSolution import CandidateSolution




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




def mutate(cs: CandidateSolution, rate=None) -> CandidateSolution:
    if rate is None:
        rate = 1/len(cs.genotype)
    new_geno = [ (1-x) if random.random() < rate else x for x in cs.genotype ]
    new_cs = CandidateSolution(genotype=new_geno, fitness_evaluator= cs.fitness_evaluator)
    return new_cs



def improve(cs: CandidateSolution) -> CandidateSolution:
    if cs.fitness is None:
        cs.evaluate()
    rate = 1/len(cs.genotype)
    #rate = 0.5
    mutated = [ (1-x) if random.random() < rate else x for x in cs.genotype ]
    new_cs = CandidateSolution(genotype=mutated, fitness_evaluator=cs.fitness_evaluator)
    new_cs.evaluate()
    return new_cs if new_cs.fitness > cs.fitness else cs




def replace(pop: list, cs) -> list:
    smallest = min(pop, key=lambda item: item.fitness)
    for i in range(len(pop)):
        if pop[i].fitness == smallest.fitness:
            break
    pop.pop(i)
    pop.append(cs)
    return pop




def select_both(p: list, kt=2):
    pool = random.sample(p,k=kt*2)
    mid = len(pool)//2
    pool1 = pool[:mid]
    pool2 = pool[mid:]
    p1 = max(pool1, key=lambda item: item.fitness)
    p2 = max(pool2, key=lambda item: item.fitness)
    return p1, p2

def select_one(p, kt=2):
    pool = random.sample(p,k=kt)
    return max(pool, key=lambda item: item.fitness)

def pareto_dominates(cs1: CandidateSolution, cs2:CandidateSolution):
    size=len(cs1.outcome)
    for i in range(size):
        if cs1.outcome[i] < cs2.outcome[i]:
            return False
    return True
    
def are_pareto_incomparable(cs1: CandidateSolution, cs2:CandidateSolution):
    return not (pareto_dominates(cs1, cs2) or pareto_dominates(cs2, cs1))
    
def select_pareto(p: list, kt=2):
    pool = random.sample(p,k=kt) # here kt is the size of the pool from which we select BOTH parents
    matrix = []
    size = len(pool)
    only_falses = True
    list_of_incomparables_coordinates = []
    for a in range(size):
        row = []
        for b in range(size):
            question = are_pareto_incomparable(pool[a], pool[b])
            row.append(question)
            if question:
                only_falses = False
                list_of_incomparables_coordinates.append((a,b))
        matrix.append(row)

    if only_falses:
        # return two random parents from the pool
        #print("no incomparable parents found")
        #p1 = random.choice(pool)
        #p2 = random.choice(pool)
        # use fitness-based selection instead
        p1 = select_one(p, kt)
        p2 = select_one(p, kt)
    else:
        #print()
        # find two incomparables
        a,b = random.choice(list_of_incomparables_coordinates)
        p1 = pool[a]
        p2 = pool[b]
    return p1,p2
            
    

    
def diversify_random_immigrant(p: list, fitness_evaluator: FitnessEvaluator):
    for _ in range(len(p) // 10):
        new_cs = CandidateSolution(len(p[0].genotype), fitness_evaluator=fitness_evaluator)
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p
    



def diversify_cached_random_immigrant(p: list, fitness_evaluator: FitnessEvaluator):
    pool = list(fitness_evaluator.fitness_cache)
    for i in range(len(p) // 10):
        rnd_geno = list(random.choice(pool))        
        new_cs = CandidateSolution( genotype=rnd_geno, 
                                    fitness_evaluator=fitness_evaluator)
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p
        



def diversify_cached_random_immigrant_with_criterion(p: list, fitness_evaluator: FitnessEvaluator):
    #select from cache genos that are incomparable to most of the population or pareto-dominate
    for i in range(len(p) // 10):
        fitness_cache_as_list = list(fitness_evaluator.fitness_cache)
        rnd_geno1 = list(random.choice(fitness_cache_as_list))
        rnd_geno2 = list(random.choice(fitness_cache_as_list))
        cs1 = CandidateSolution(genotype=rnd_geno1, fitness_evaluator=fitness_evaluator)
        cs2 = CandidateSolution(genotype=rnd_geno2, fitness_evaluator=fitness_evaluator)
        
        # The following should not be doing anything due to being cached
        cs1.evaluate()
        cs2.evaluate()

        #counter1 = 0
        #counter2 = 0
        #for individual in p: 
        #    if are_pareto_incomparable(cs1, individual):
        #        counter1 += 1
        #    if are_pareto_incomparable(cs2, individual):
        #        counter2 += 1
        counter1 = sum([1 if are_pareto_incomparable(cs1, individual) else 0 for individual in p])
        counter2 = sum([1 if are_pareto_incomparable(cs2, individual) else 0 for individual in p])


        #if counter1 > counter2:
        #    new_cs = cs1
        #else:
        #    new_cs = cs2
        new_cs = cs1 if counter1 > counter2 else cs2    
        
        p = replace(p, new_cs)
    return p




def evolve( max_iterations, pop_size, kt, geno_size, 
            local_search=False,
            random_immigrant=False,
            pareto_select=False,
            mutation_rate=None, 
            crossover_rate=None, 
            fitness_evaluator=None):    
    pop = []
    for _ in range(pop_size):
        cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
        cs.evaluate()
        pop.append(cs)
        
    best = max(pop, key=lambda item: item.fitness)

    for iteration in range(max_iterations):
        #print(f"Iteration #{iteration}")
        if pareto_select:
            p1,p2 = select_pareto(pop, 5)
        else:
            p1 = select_one(pop, kt)
            p2 = select_one(pop, kt)
            #p1,p2 = select_both(pop, kt)

        os1, os2 = recombine(p1,p2, rate=crossover_rate)
        
        if local_search:
            os1 = improve(os1)
            os2 = improve(os2)
    
        os1 = mutate(os1, rate=mutation_rate)
        os2 = mutate(os2, rate=mutation_rate)
    
        os1.evaluate()
        os2.evaluate()

        if random_immigrant:
            #pop = diversify_cached_random_immigrant_with_criterion(pop, fitness_evaluator)
            #pop = diversify_cached_random_immigrant(pop, fitness_evaluator)
            pop = diversify_random_immigrant(pop, fitness_evaluator)
        
        pop = replace(pop, os1)
        pop = replace(pop, os2)

        best = max(pop, key=lambda item: item.fitness)
        if best.fitness >= fitness_evaluator.max_fitness:
            break

    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (best.fitness, iteration) + cache_usage

