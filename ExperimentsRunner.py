from FitnessEvaluator import FitnessEvaluator
from SteadyStateGeneticAlgorithm import evolve

def OneMax(genotype):
    return sum(genotype)

def ZeroMax(genotype):
    return len(genotype) - sum(genotype)


if __name__ == '__main__':
    
    results = []
    
    for i in range(5):
        fitness_evaluator = FitnessEvaluator(OneMax, 1000)
        
        #evolve(geno_size=100, max_iterations=400, pop_size=25, kt=2)
        #result = evolve(geno_size=1000, max_iterations=8000, pop_size=25, kt=2, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
        result = evolve(geno_size=1000, max_iterations=10_000, pop_size=25, kt=2, crossover_rate=0.8, fitness_evaluator=fitness_evaluator)
        #evolve(geno_size=10000, max_iterations=80000, pop_size=25, kt=5)
        
        print(f"Run #{i}",result)
        #print("\nBest Candidate Solution:", results[0], "@ iteration #", results[1])
        #print("FitnessCache usage:", results[2], results[3])
        results.append(result)

    print([r for (_, r, _, _) in results])
    #TODO - run experiments on OneMax / ZeroMax and perform statistical test
    # see https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/
