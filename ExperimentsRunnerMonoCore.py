from FitnessEvaluator import FitnessEvaluator, DualFitnessEvaluator
from AlgorithmSteadyStateGeneticAlgorithm import evolve as evolve_ssga
from AlgorithmOnePlusOneGeneticAlgorithm import evolve as evolve_1plus1ga
from scipy.stats import mannwhitneyu
from scipy.stats import shapiro
from scipy.stats import ttest_ind
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
    #number_of_trials = 32

    #for file uf250-32.cnf (hardcoded in FitnessSAT.py) 1065 clauses, 250 variables
    number_of_trials = 32
    MAX_ITERATIONS = 100_000

    random.seed(422399)
    
    fitness_evaluator = FitnessEvaluator(FitnessSAT.evaluate_formula, FitnessSAT.MAX_FITNESS)
    #dual_fitness_evaluator = DualFitnessEvaluator(FitnessSAT.evaluate_formula, 91)
    
    #from rich.progress import track
    #import time

    results = []
    start_experiment = timeit.default_timer()

    #for i in track(range(number_of_trials), description='Experiments Running'):        
    

    experiments_best_plot = [0.0 for _ in range(MAX_ITERATIONS)]
    for i in range(number_of_trials):        
        print(f"Run #{i}", end='\t')
        print(f"Started", end='\t', flush=True)
        start_trial = timeit.default_timer()
        # best, iteration, cache_hits, cache_misses = evolve_1plus1ga(    
        #                     #geno_size=20, # for uf20-04.cnf
        #                     geno_size=100, # for uf100-04.cnf
        #                     #mutation_rate = 0.75,
        #                     #max_iterations=40_000, # for uf20-04.cnf
        #                     max_iterations=MAX_ITERATIONS, # for uf100-04.cnf
        #                     improve_method="by_reset",
        #                     #recombination=10,
        #                     fitness_evaluator=fitness_evaluator, 
        #                     experiment_number=i,
        #                     experiment_total=number_of_trials)
        best, iteration, cache_hits, cache_misses, best_plot  = evolve_ssga(       
                            geno_size=20, # for uf20-04.cnf
                            #geno_size=100, # for uf100-04.cnf
                            #geno_size=250, # for uf250-32.cnf
                            max_iterations=MAX_ITERATIONS, 
                            pop_size=25, # for uf20-04.cnf
                            #pop_size=50, # for uf100-04.cnf
                            kt=2, 
                            #local_search=True,
                            crossover_rate=1.0, 
                            #random_immigrant= 'original', #'cached' #'cached+criterion'
                            #pareto_select=True,
                            mutation_rate=0.05, 
                            fitness_evaluator=fitness_evaluator, 
                            experiment_number=i,
                            experiment_total=number_of_trials)
        stop_trial = timeit.default_timer()
        result = tuple([best, iteration, cache_hits, cache_misses])
        results += [result]
        for i in range(MAX_ITERATIONS):
            experiments_best_plot[i] += best_plot[i]

        print(f"DONE\t ({time_warp(stop_trial - start_trial)})")
    
    # the average of all the best fitness averages at each iteration over all runs 
    experiments_best_plot_average = 0.0
    
    #averaging the best fitness for every iteration over all the runs
    for i in range(MAX_ITERATIONS):
        experiments_best_plot[i] = experiments_best_plot[i] / number_of_trials
        experiments_best_plot_average += experiments_best_plot[i]

    # NOTE the number of the stat file is len(results[0]) 
    # so, if we have 4 stats, it will come after stats0 to stats3
    experiments_best_plot_average /= MAX_ITERATIONS
    with open(f'stat{len(results[0])}.pickle', 'wb') as f: 
        pickle.dump(experiments_best_plot, f)

    stop_experiment = timeit.default_timer()


    for stat in range(len(results[0])):
        series = [r[stat] for r in results]

        with open(f'stat{stat}.pickle', 'wb') as f:
            pickle.dump(series,f)

    # NOTE same as stat[len(results[0])]
    with open(f'experiment_best_plot.pickle', 'wb') as f: 
        pickle.dump(experiments_best_plot, f)
    
    print(f'Average of all the best fitness at each iteration, over all runs: '
          f'{experiments_best_plot_average}')
    print("Run duration =", time_warp(stop_experiment-start_experiment))


