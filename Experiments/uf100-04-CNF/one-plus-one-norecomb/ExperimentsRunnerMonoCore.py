from FitnessEvaluator import FitnessEvaluator, DualFitnessEvaluator
from AlgorithmSteadyStateGeneticAlgorithm import evolve as evolve_ssga
from Deprecated.AlgorithmOnePlusOneGeneticAlgorithm import evolve as evolve_1plus1ga
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
import random
import timeit
import pickle

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)

import FitnessSAT

def time_warp(seconds):
    minutes = seconds // 60 
    seconds = seconds % 60 
    hours = minutes // 60 
    minutes = minutes % 60 
    return '' + str(int(hours)) + ':' + str(int(minutes)) + ':' + str(int(seconds))

if __name__ == '__main__':
        
    #for file uf20-04.cnf (hardcoded in FitnessSAT.py) 91 clauses, 20 variables (genolength)
    # number_of_trials = 25
    
    #for file uf100-04.cnf (hardcoded in FitnessSAT.py) 430 clauses, 100 variables
    number_of_trials = 40
    
    random.seed(422399)
    
    fitness_evaluator = FitnessEvaluator(FitnessSAT.evaluate_formula, FitnessSAT.MAX_FITNESS)
    #dual_fitness_evaluator = DualFitnessEvaluator(FitnessSAT.evaluate_formula, 91)
    

    results = []
    start_experiment = timeit.default_timer()

    for i in range(number_of_trials):        
        print(f"Run #{i}", end='\t')
        print(f"Started", end='\t')
        start_trial = timeit.default_timer()
        best, iteration, cache_hits, cache_misses = evolve_1plus1ga(    
                            #geno_size=20, # for uf20-04.cnf
                            geno_size=100, # for uf100-04.cnf
                            #mutation_rate = 0.75,
                            #max_iterations=40_000, # for uf20-04.cnf
                            max_iterations=80_000, # for uf100-04.cnf
                            improve_method="by_reset",
                            #recombination=10,
                            fitness_evaluator=fitness_evaluator)
        #best, iteration, cache_hits, cache_misses  = evolve_ssga(       
        #                    #geno_size=20, # for uf20-04.cnf
        #                    geno_size=100, # for uf100-04.cnf
        #                    max_iterations=400_000, 
        #                    #pop_size=25, # for uf20-04.cnf
        #                    pop_size=50, # for uf100-04.cnf
        #                    kt=2, 
        #                    #local_search=True,
        #                    crossover_rate=1.0, 
        #                    #random_immigrant=True,
        #                    pareto_select=True,
        #                    #mutation_rate=0.50, 
        #                    fitness_evaluator=fitness_evaluator)
        stop_trial = timeit.default_timer()
        result = tuple([best, iteration, cache_hits, cache_misses])
        results += [result]
        print(f"DONE\t ({time_warp(stop_trial - start_trial)})")
    
    stop_experiment = timeit.default_timer()


    for stat in range(len(results[0])):
        series = [r[stat] for r in results]

        with open(f'stat{stat}.pickle', 'wb') as f:
            pickle.dump(series,f)


    print("Run duration =", time_warp(stop_experiment-start_experiment))


