from FitnessEvaluator import FitnessEvaluator
from SteadyStateGeneticAlgorithm import evolve as evolve_ssga
from OnePlusOneGeneticAlgorithm import evolve as evolve_1plus1ga
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
import numpy
import random
from concurrent.futures import ProcessPoolExecutor

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)

import sat


if __name__ == '__main__':
    
    number_of_cores = 4
    number_of_trials = 25
    random.seed(422399)

    results1 = []
    results2 = []
    
    # SAT
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    
    for i in range(number_of_trials):        
        print(f"Algo #1 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate = 0.75,
                                        max_iterations=400_000, 
                                        improve_method="by_tabu_reset",
                                        fitness_evaluator=fitness_evaluator))
                    # executor.submit(    evolve_ssga, 
                    #                     geno_size=20, 
                    #                     max_iterations=400_000, 
                    #                     pop_size=25, 
                    #                     kt=2, 
                    #                     local_search=True,
                    #                     crossover_rate=1.0, 
                    #                     fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        results += [tuple(r.result()) for r in futures]    
        results1 += [tuple(r) for r in results]
        print(f"DONE")
    
    for i in range(number_of_trials):        
        print(f"Algo #2 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate=0.75,
                                        max_iterations=400_000, 
                                        improve_method="by_reset",
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        for core in range(number_of_cores):
            results.append(futures[core].result())    
        results2 += [tuple(r) for r in results]
        print(f"DONE")
 


    for stat in range(len(results1[0])):
        #series1 = [r for (_, r, _, _) in results1]
        #series2 = [r for (_, r, _, _) in results2]
        series1 = [r[stat] for r in results1]
        series2 = [r[stat] for r in results2]
        print(f"\n\nStatistic #{stat}")
        print("\tSeries 1 mean =", numpy.mean(series1))
        print("\tSeries 2 mean =", numpy.mean(series2))
        
        # Performing statistical test
        # see https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/

        stat, p = shapiro(series1)
        print('\tShapiro: \t stat=%10.3f, p=%10.3f \t --> ' % (stat, p), end="")
        if p > 0.05:
            print('Probably Gaussian')
        else:
            print('Probably not Gaussian')

        stat, p = ttest_ind(series1, series2)
        print('\tStudent T: \t stat=%10.3f, p=%10.3f \t --> ' % (stat, p), end="")
        if p > 0.05:
            print('SAME distribution')
        else:
            print('DIFFERENT distributions')

        stat, p = mannwhitneyu(series1, series2)
        print("\tMann-Whitney: \t stat=%10.3f, p=%10.3f \t --> " % (stat, p), end="")
        if p > 0.05:
            #print('H0 not rejected: samples are from SAME distribution')
            print('SAME distribution')
        else:
            #print('H0 rejected: samples are from DIFFERENT distribution')
            print('DIFFERENT distribution')
