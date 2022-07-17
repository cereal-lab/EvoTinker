import random
from FitnessEvaluator import fitness_evaluator


class CandidateSolution(object):
    
    def __init__(self, length=None, genotype=None):
        if genotype is None:
            self.genotype = []
            for _ in range(length):
                self.genotype.append(random.randint(0,1))
        else:
            self.genotype = genotype
        self.fitness = None
        
    def evaluate(self):
        #self.fitness = FitnessEvaluator().evaluate(self.genotype)
        self.fitness = fitness_evaluator.evaluate(self.genotype)
    
    def __repr__(self):
        return f"<{self.genotype}>"




def recombine(p1: CandidateSolution, p2: CandidateSolution):
    mask = [0 if random.random() < 0.5 else 1 for _ in range(len(p1.genotype))]
    os1 = [p1.genotype[i] if mask[i] == 0 else p2.genotype[i]
           for i in range(len(mask))]
    os2 = [p1.genotype[i] if mask[i] == 1 else p2.genotype[i]
           for i in range(len(mask))]
    return os1,os2




def mutate(cs, rate=None):
    if rate is None:
        rate = 1/len(cs)
        #rate = random.randint(1,len(cs)//4)/len(cs)
    return [x if random.random() >= rate else (1-x) for x in cs ]




def replace(pop, cs):
    smallest = min(pop, key=lambda item: item.fitness)
    for i in range(len(pop)):
        if pop[i].fitness == smallest.fitness:
            break
    pop.pop(i)
    pop.append(cs)
    return pop




def select(p, kt=2):
    pool = random.sample(p,k=kt)
    return max(pool, key=lambda item: item.fitness)




def diversify(p: list):
    #hypermutation wannabe
    #for _ in range(pop_size // 5):
    #    new_cs = CandidateSolution(geno_size)
    #    new_cs.evaluate()
    #    pop = replace(pop, new_cs)
    for _ in range(len(p) // 10):
        new_cs = CandidateSolution(genotype=list(random.choice(list(fitness_evaluator.fitness_cache))))
        new_cs.evaluate()
        p = replace(p, new_cs)
    return p
        



def evolve(max_iterations, pop_size, kt, geno_size):
    pop = []
    for _ in range(pop_size):
        pop.append(CandidateSolution(geno_size))
    for i in range(pop_size):
        pop[i].evaluate()
        
    best = max(pop, key=lambda item: item.fitness)
    #print(f"Iteration #0:", best.fitness)

    for iteration in range(max_iterations):
        p1 = select(pop, kt)
        p2 = select(pop, kt)

        os1, os2 = recombine(p1,p2)

        os1 = mutate(os1)
        os2 = mutate(os2)

        cs1 = CandidateSolution(genotype=os1)
        cs2 = CandidateSolution(genotype=os2)
        cs1.evaluate()
        cs2.evaluate()
        
        #pop = diversify(pop)
        
        pop = replace(pop, cs1)
        pop = replace(pop, cs2)

        best = max(pop, key=lambda item: item.fitness)
        #print(f"Iteration #{iteration}:", best.fitness)

    print("\nBest Candidate Solution:", best.fitness)
    #print("FitnessCache usage:", FitnessEvaluator().report_cache_usage())
    print("FitnessCache usage:", fitness_evaluator.report_cache_usage())
    #FitnessEvaluator().zero_cache_usage()
    #print(fitness_evaluator.fitness_cache)
    fitness_evaluator.zero_cache_usage()




if __name__ == '__main__':
    #evolve(geno_size=100, max_iterations=400, pop_size=25, kt=2)
    evolve(geno_size=1000, max_iterations=8000, pop_size=25, kt=2)
    #print(16025 / 2**1000)
