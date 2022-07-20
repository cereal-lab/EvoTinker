from FitnessEvaluator import FitnessEvaluator
from SteadyStateGeneticAlgorithm import evolve

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)


if __name__ == '__main__':
    
    fitness_evaluator = FitnessEvaluator(OneMax, 1000)
    
    #evolve(geno_size=100, max_iterations=400, pop_size=25, kt=2)
    results = evolve(geno_size=1000, max_iterations=8000, pop_size=25, kt=2, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
    #evolve(geno_size=10000, max_iterations=80000, pop_size=25, kt=5)
    
    print(results)

