from FitnessEvaluator import FitnessEvaluator, DualFitnessEvaluator
from SteadyStateGeneticAlgorithm import evolve as evolve_ssga
from OnePlusOneGeneticAlgorithm import evolve as evolve_1plus1ga
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
import numpy
import random
from concurrent.futures import ProcessPoolExecutor
import timeit
import pickle

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)

import FitnessSAT


if __name__ == '__main__':
    
    number_of_cores = 4
    number_of_trials = 25
    random.seed(422399)

    results1 = []
    
    fitness_evaluator = FitnessEvaluator(FitnessSAT.evaluate_formula, 91)
    #dual_fitness_evaluator = DualFitnessEvaluator(FitnessSAT.evaluate_formula, 91)
    

    start1 = timeit.default_timer()

    for i in range(number_of_trials):        
        print(f"Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    #executor.submit(    evolve_1plus1ga, 
                    #                    geno_size=20, 
                    #                    #mutation_rate = 0.75,
                    #                    max_iterations=40_000, 
                    #                    improve_method="by_reset",
                    #                    recombination=10,
                    #                    fitness_evaluator=fitness_evaluator))
                    executor.submit(    evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=4, 
                                        #local_search=True,
                                        crossover_rate=1.0, 
                                        #random_immigrant=True,
                                        pareto_select=True,
                                        #mutation_rate=0.50, 
                                        fitness_evaluator=fitness_evaluator))

            #local_search=False,
            
            #fitness_evaluator=None): 
            print(f"Started", end='\t')
        results = []
        results += [tuple(r.result()) for r in futures]    
        results1 += [tuple(r) for r in results]
        print(f"DONE")
    
    stop1 = timeit.default_timer()


    for stat in range(len(results1[0])):
        series1 = [r[stat] for r in results1]

        with open(f'stat{stat}.pickle', 'wb') as f:
            pickle.dump(series1,f)


    print("Run duration =", stop1-start1)
