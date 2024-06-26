import random
import numpy
from FitnessEvaluator import FitnessEvaluator
from CandidateSolution import CandidateSolution
#----
from rich.progress import track
import time
import EvoConfig



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
    pool = fitness_evaluator.fitness_cache
    for i in range(len(p) // 10):
        rnd_geno = list(pool.random_key())        
        new_cs = CandidateSolution( genotype=rnd_geno, 
                                    fitness_evaluator=fitness_evaluator)
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p

def diversify_cached_random_immigrant_with_criterion_FITNESS(p: list, fitness_evaluator: FitnessEvaluator):
    # select from cache genos that have high fitness
    for i in range(len(p) // 10):
        # NOTE: The 10 below is the KT for selecting from cache
        L_geno = [list(fitness_evaluator.fitness_cache.random_key()) for _ in range(10)]

        L_cs = [CandidateSolution(genotype=rnd_geno, fitness_evaluator=fitness_evaluator) for rnd_geno in L_geno]
        for c in L_cs: 
            c.evaluate()
            # should not be doing anything due to being cached
        
        p = replace(p, max(L_cs, key=lambda x : x.fitness))
    return p


def hamming(c1, c2): 
    # returns the hamming distance between the genotypes of candidate solutions c1 and c2
    return sum([abs(c1.genotype[i] - c2.genotype[i]) for i in range(len( c1.genotype ))])

def diversify_cached_random_immigrant_with_criterion_HAMMING(p: list, fitness_evaluator: FitnessEvaluator):
    # select from cache genos that on average maximally distant from population genotypes
    # uses the hamming distance as measure of distance
    for i in range(len(p) // 10):
        # NOTE: The 10 below is the KT for selecting from cache
        L_geno = [list(fitness_evaluator.fitness_cache.random_key()) for _ in range(10)]

        L_cs = [CandidateSolution(genotype=rnd_geno, fitness_evaluator=fitness_evaluator) for rnd_geno in L_geno]
        for c in L_cs: 
            c.evaluate()
            # should not be doing anything due to being cached
        
        avg_dist = []
        for cs in L_cs: 
            tmp_dist = [hamming(cs, individual) for individual in p]
            avg_dist.append(sum(tmp_dist)/len(tmp_dist))
                
        max_dist = avg_dist[0]
        max_indx = 0
        for i,avg in enumerate(avg_dist): 
            if avg > max_dist: 
                max_dist = avg
                max_indx = i
                
        p = replace(p, L_cs[max_indx])
    return p


def diversify_cached_random_immigrant_with_criterion_PARETO(p: list, fitness_evaluator: FitnessEvaluator):
    #select from cache genos that are incomparable to most of the population or pareto-dominate
    for i in range(len(p) // 10):
        rnd_geno1 = list(fitness_evaluator.fitness_cache.random_key())
        rnd_geno2 = list(fitness_evaluator.fitness_cache.random_key())
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
            random_immigrant='',
            pareto_select=False,
            mutation_rate=None, 
            crossover_rate=None, 
            fitness_evaluator=None, 
            experiment_number=None,
            number_of_trials=None, 
            **kwargs):    
    pop = []
    for _ in range(pop_size):
        cs = CandidateSolution(geno_size, fitness_evaluator=fitness_evaluator)
        cs.evaluate()
        pop.append(cs)
        
    best = max(pop, key=lambda item: item.fitness)
    if experiment_number != None and number_of_trials != None: 
        descript = f'SSGA {experiment_number:3d} /{number_of_trials:3d}'
    else:
        descript = 'SSGA' 

    # NOTE: TODO: Pick an iterator: 
    it = track(range(max_iterations), description=descript) # for interactive shells
    # it = range(max_iterations) # for background batch jobs
    threshold = EvoConfig.config['DOP_epoch_duration']
    experiment_plot_best = []
    fitness_evaluator.reset_formula()
    for iteration in it:
        if iteration % threshold == 0:
            fitness_evaluator.next_formula(iteration // threshold)
            for p in pop: 
                p.evaluate()

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

        if random_immigrant == 'original':
            pop = diversify_random_immigrant(pop, fitness_evaluator)
        elif random_immigrant == 'cached':
            pop = diversify_cached_random_immigrant(pop, fitness_evaluator)
        elif random_immigrant == 'cached+criterion':
            pop = diversify_cached_random_immigrant_with_criterion_FITNESS(pop, fitness_evaluator)
            # NOTE the above can be changed to _PARETO _FITNESS _HAMMING
        elif random_immigrant != '':
            print('Unknown Random Immigrant Method')
            exit()

        pop = replace(pop, os1)
        pop = replace(pop, os2)

        best = max(pop, key=lambda item: item.fitness)
        
        experiment_plot_best.append(best.fitness)
        
        # NOTE we deactivate the breaking early if global optimum is found
        # while we use time-dependent environments 
        #if best.fitness >= fitness_evaluator.max_fitness:
        #    break

    cache_usage = fitness_evaluator.report_cache_usage()
    fitness_evaluator.zero_cache_usage()
    return (best.fitness, iteration) + cache_usage + (experiment_plot_best,)

