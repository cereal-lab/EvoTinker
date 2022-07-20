from FitnessEvaluator import FitnessEvaluator
from SteadyStateGeneticAlgorithm import evolve
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
import numpy

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)


if __name__ == '__main__':
    
    number_of_trials = 100
    results1 = []
    results2 = []
    fitness_evaluator = FitnessEvaluator(OneMax, 1000)
    #fitness_evaluator = FitnessEvaluator(OneMax, 1000)
    for i in range(number_of_trials):
        #result = evolve(geno_size=100, max_iterations=400, pop_size=25, kt=2, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
        #result = evolve(geno_size=1000, max_iterations=8000, pop_size=25, kt=2, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
        result1 = evolve(   geno_size=1000, 
                            max_iterations=10_000, 
                            pop_size=25, 
                            kt=2, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator, 
                            select_old_method=True)
        result2 = evolve(   geno_size=1000,
                            max_iterations=10_000, 
                            pop_size=25, 
                            kt=2, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator,
                            select_old_method=False)
        #result = evolve(geno_size=10000, max_iterations=80000, pop_size=25, kt=5, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)

    series1 = [r for (_, r, _, _) in results1]
    series2 = [r for (_, r, _, _) in results2]

    print("Series 1 mean =", numpy.mean(series1))
    print("Series 2 mean =", numpy.mean(series2))
    
    # Performing statistical test
    # see https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/

    print("Shapiro")
    stat, p = shapiro(series1)
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('Probably Gaussian')
    else:
        print('Probably not Gaussian')

    print("Student T test")
    stat, p = ttest_ind(series1, series2)
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('Probably the SAME distribution')
    else:
        print('Probably DIFFERENT distributions')
        
    print("Mann-Whitney")
    stat, p = mannwhitneyu(series1, series2)
    print(stat,p)
    if p > 0.05:
        print('H0 not rejected: samples are from SAME distribution')
    else:
        print('H0 rejected: samples are from DIFFERENT distribution')


